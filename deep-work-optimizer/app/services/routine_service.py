import requests

ROUTINE_API_URL = "https://student-d-api-url.com/stability"

def get_routine_stability(data):

    try:
        response = requests.post(ROUTINE_API_URL, json=data, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception:
        return {"stability_score": 50, "warning": "Routine API unavailable"}