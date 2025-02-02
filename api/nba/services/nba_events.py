from django.http import JsonResponse
from oddsApi.settings import API_KEY, NBA_EVENTS_API_URL
import requests

def get_nba_events(request):
    """
    Fetch all upcoming NBA games with their event IDs.
    """
    params = {
        "apiKey": API_KEY,
    }

    try:
        response = requests.get(NBA_EVENTS_API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, dict) and "events" in data:
            data = data["events"]
        
        return [event["id"] for event in data]

    except requests.exceptions.RequestException as e:
        print(f"Error fetching NBA events: {e}")  # Log error for debugging
        return []