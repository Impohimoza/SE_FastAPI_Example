import requests

API_URL = "http://127.0.0.1:8000"

def analyze_text(text: str):
    """
    Анализ одного текста через API.
    """
    response = requests.post(f"{API_URL}/predict/", json={"text": text})
    response.raise_for_status() 
    return response.json()