from oddsApi.settings import API_KEY, NBA_PLAYER_PROPS_URL
from ..utils import *
import requests

def get_nba_player_props_odds(request, event_id):
    """
    Fetch player props for a given NBA event ID and structure them by player.
    """
    player_name_filter = request.GET.get("player_name", None)  # Optional player filter
    params = {
        "apiKey": API_KEY,
        "regions": NBA_PLAYER_ODDS_REGIONS,  # US bookmakers
        "markets": NBA_PLAYER_MARKETS, # Fetch player props
        "oddsFormat": NBA_PLAYER_ODDS_FORMAT,  # Decimal odds format
    }

    try:
        url = NBA_PLAYER_PROPS_URL.format(eventId=event_id)
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        # Dictionary to store players and their props
        player_props = {}

        for bookmaker in data.get("bookmakers", []):
            bookmaker_name = bookmaker.get("key", "")

            if bookmaker_name not in NBA_BOOKMAKERS:
                continue

            for market in bookmaker.get("markets", []):
                market_name = market.get("key", "unknown_market")
                for outcome in market.get("outcomes", []):
                    player_name = outcome["description"]
                    lean = outcome["name"]
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
                        "lean": lean,
                        "market": market_name,
                        "point": point,
                        "odds": odds,
                        "bookmaker": bookmaker["title"]
                    })

        return {"player_props": player_props}

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}