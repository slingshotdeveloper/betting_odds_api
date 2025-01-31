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

        # Extract event IDs
        events = [{"id": event["id"], "matchup": f"{event['home_team']} vs {event['away_team']}"} for event in data]

        return JsonResponse({"nba_events": events}, safe=False)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)