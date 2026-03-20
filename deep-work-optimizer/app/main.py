from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import requests
import os

app = FastAPI()

# -----------------------------
# CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Weather API
# -----------------------------
OPENWEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
CITY = "Dublin"

# -----------------------------
# Classmate API
# -----------------------------
STABILITY_API_URL = "https://2u736o5k8k.execute-api.us-east-1.amazonaws.com/prod/api/stability"


# -----------------------------
# Input model
# -----------------------------
class UserInput(BaseModel):
    sleep_hours: float
    study_hours: float
    time_of_day: str


# -----------------------------
# Health check
# -----------------------------
@app.get("/")
def health():
    return {"status": "healthy"}


# -----------------------------
# Serve frontend
# -----------------------------
@app.get("/app")
def serve_frontend():
    return FileResponse("index.html")


# -----------------------------
# Get weather
# -----------------------------
def get_weather():
    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={OPENWEATHER_API_KEY}&units=metric"

    try:
        r = requests.get(url)
        data = r.json()

        temp = data["main"]["temp"]
        condition = data["weather"][0]["main"]

        return temp, condition

    except:
        return None, None


# -----------------------------
# Get routine stability
# -----------------------------
def get_routine_stability():

    payload = {
        "user_id": "deepwork-user",
        "sleep": {
            "sleep_times": ["23:00","23:15","23:30"],
            "wake_times": ["07:00","07:10","07:15"]
        },
        "meals":[
            {"breakfast":"08:00","lunch":"13:00","dinner":"19:00"}
        ],
        "exercise":{
            "frequency_per_week":3,
            "duration_minutes":40,
            "types":["running"]
        }
    }

    try:
        r = requests.post(STABILITY_API_URL, json=payload)
        data = r.json()

        score = data["routine_stability_index"]["overall_score"]
        label = data["routine_stability_index"]["label"]

        return score, label

    except:
        return None, None


# -----------------------------
# Main API
# -----------------------------
@app.post("/optimize-session")
def optimize_session(data: UserInput):

    focus_score = data.sleep_hours * 10

    if data.time_of_day.lower() == "morning":
        focus_score += 10
    elif data.time_of_day.lower() == "night":
        focus_score -= 10

    focus_score -= data.study_hours * 5

    # Weather
    temperature, condition = get_weather()

    if temperature:
        if temperature > 30:
            focus_score -= 10
        elif 20 <= temperature <= 25:
            focus_score += 5

    if condition and condition.lower() == "rain":
        focus_score -= 5

    # Classmate API
    stability_score, stability_label = get_routine_stability()

    focus_score = max(0, min(100, focus_score))

    if focus_score > 80:
        session_length = 90
    elif focus_score > 60:
        session_length = 60
    else:
        session_length = 30

    return {
        "focus_score": round(focus_score,2),
        "recommended_session_length": session_length,
        "weather":{
            "temperature": temperature,
            "condition": condition
        },
        "routine_stability":{
            "score": stability_score,
            "label": stability_label
        }
    }