from oddsApi.settings import API_KEY, NFL_PLAYER_PROPS_URL
from ..utils import *
import requests

def get_nfl_player_props_odds(request, event_id):
    """
    Fetch player props for a given NFL event ID and structure them by player.
    """
    player_name_filter = request.GET.get("player_name", None)  # Optional player filter
    params = {
        "apiKey": API_KEY,
        "regions": NFL_PLAYER_ODDS_REGIONS,  # US bookmakers
        "markets": NFL_PLAYER_MARKETS, # Fetch player props
        "oddsFormat": NFL_PLAYER_ODDS_FORMAT,  # Decimal odds format
    }

    try:
        url = NFL_PLAYER_PROPS_URL.format(eventId=event_id)
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        # Dictionary to store players and their props
        player_props = {}

        for bookmaker in data.get("bookmakers", []):
            for market in bookmaker.get("markets", []):
                market_name = market.get("key", "unknown_market")
                for outcome in market.get("outcomes", []):
                    player_name = outcome["description"]
                    selection = outcome["name"]
                    odds = outcome["price"]
                    point = outcome["point"]
                    key = player_name  # Use player name as the key

                    # Filter by player name if specified
                    if player_name_filter and player_name_filter.lower() not in player_name.lower():
                        continue  # Skip this player if name filter doesn't match

                    # If player isn't in the dictionary, initialize their list
                    if key not in player_props:
                        player_props[key] = []

                    # Add the player's prop with bookmaker info
                    player_props[key].append({
                        "selection": selection,
                        "market": market_name,
                        "point": point,
                        "odds": odds,
                        "bookmaker": bookmaker["title"]
                    })

        return {"player_props": player_props}

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}