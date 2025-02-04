from django.http import JsonResponse
from oddsApi.settings import API_KEY, NBA_PLAYER_PROPS_URL
import requests
from ..utils import *

def get_dfs_player_props_lines(request, event_id):
    """
    Fetch player prop lines for underdog and prizepicks from the US DFS region.
    Always removes the 'under' and keeps only the 'over' for each player/bookmaker.
    The response includes only the 'bookmaker' and 'point_line'.
    """

    params = {
        "apiKey": API_KEY,
        "regions": NBA_PLAYER_DFS_REGIONS,  # US DFS bookmakers (underdog, prizepicks)
        "markets": NBA_PLAYER_MARKETS,  # Fetch player props
        "oddsFormat": NBA_PLAYER_ODDS_FORMAT,  # Odds format
    }

    try:
        url = NBA_PLAYER_PROPS_URL.format(eventId=event_id)
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        player_props = {}

        for bookmaker in data.get("bookmakers", []):
            for market in bookmaker.get("markets", []):
                market_name = market.get("key", "unknown_market")
                for outcome in market.get("outcomes", []):
                    player_name = outcome["description"]
                    prop_line = outcome["point"]
                    bookmaker_name = bookmaker["title"]
                    lean = outcome["name"].lower()  # 'over' or 'under'

                    # If the player is not in the dictionary, initialize an empty list for them
                    if player_name not in player_props:
                        player_props[player_name] = []

                    if lean == "over":
                        player_props[player_name].append({
                            "bookmaker": bookmaker_name,
                            "market": market_name,
                            "prop_line": prop_line,
                        })

        return {"player_props": player_props}

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}