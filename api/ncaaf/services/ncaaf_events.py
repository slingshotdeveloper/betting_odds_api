from django.http import JsonResponse
from oddsApi.settings import API_KEY, NCAAF_EVENTS_API_URL
import requests

def get_ncaaf_events_ids(request):
    """
    Fetch all upcoming NCAAF games with their event IDs.
    """
    params = {
        "apiKey": API_KEY,
    }

    try:
        response = requests.get(NCAAF_EVENTS_API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, dict) and "events" in data:
            data = data["events"]
        
        return [event["id"] for event in data]

    except requests.exceptions.RequestException as e:
        print(f"Error fetching NCAAF events: {e}")  # Log error for debugging
        return []
    
    
def get_ncaaf_events(request):
    """
    Fetch all upcoming NCAAF games with their event IDs.
    """
    params = {
        "apiKey": API_KEY,
    }

    try:
        response = requests.get(NCAAF_EVENTS_API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        # Extract event IDs
        events = [{"id": event["id"], "matchup": f"{event['home_team']} vs {event['away_team']}"} for event in data]

        return JsonResponse({"ncaaf_events": events}, safe=False)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)