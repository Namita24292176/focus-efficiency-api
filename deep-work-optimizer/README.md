# Deep Work Session Optimizer – Student C

## Project Overview
This project is a cloud-based Deep Work Optimization system that integrates:

- Focus Efficiency Prediction API (own API)
- Routine Stability Index API (Student D)
- OpenWeather Public API

The system recommends optimized deep-work session lengths based on focus, routine stability, and environmental factors.

---

## Technologies Used

- Python (FastAPI)
- Docker
- AWS ECS
- OpenWeather API
- RESTful APIs

---

## Local Setup Instructions

### 1. Clone Repository

git clone <repository-url>

### 2. Create Virtual Environment

python -m venv venv
source venv/bin/activate   (Mac/Linux)
venv\Scripts\activate      (Windows)

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Set Environment Variables

Create a `.env` file:

WEATHER_API_KEY=your_api_key_here

### 5. Run Application

uvicorn app.main:app --reload

Open:
http://127.0.0.1:8000/docs

---

## Docker Instructions

### Build Docker Image

docker build -t focus-api .

### Run Docker Container

docker run -p 8000:80 --env-file .env focus-api

---

## Cloud Deployment

Deployed using:
- AWS ECS
- Docker containers
- Auto Scaling enabled

---

## Author

Student C  
MSc Cloud Computing  
National College of Ireland