from django.http import JsonResponse
from django.views import View
import requests
import json
from openpyxl.utils.dataframe import dataframe_to_rows
import pandas as pd
from .services.nba_events import *
from .services.nba_player_props_odds import get_nba_player_props_odds
from .services.nba_dfs_player_prop_lines import get_dfs_player_props_lines
from .utils import *

class HomeView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({"message": "Hello, World!"})
    
def get_nba_events_info(request):
    return get_nba_events(request)


def get_nba_player_props_value(request):
    """
    Combine player prop lines from Underdog and PrizePicks with matching bookmaker odds.
    Filters out bookmaker odds that don't match the DFS prop line.
    """
    try:
        event_ids = get_nba_events_ids(request)
        event_ids = [event_ids[3]] # Remove when ready for production

        underdog_props = []
        prizepicks_props = []

        for event_id in event_ids:
            player_props_odds = get_nba_player_props_odds(request, event_id).get("player_props", {})

            if not player_props_odds:
                continue
            
            dfs_data = get_dfs_player_props_lines(request, event_id).get("player_props", {})

            for player_name, dfs_lines in dfs_data.items():
                if player_name not in player_props_odds:
                    continue  # Skip if no matching bookmaker data

                for dfs_line in dfs_lines:
                    prop_line = dfs_line["prop_line"]
                    market = dfs_line["market"]
                    bookmaker = dfs_line["bookmaker"].lower()

                    matching_odds = [
                        odds for odds in player_props_odds[player_name]
                        if odds["point"] == prop_line and odds["market"] == market
                    ]

                    if not matching_odds:
                        continue

                    player_entry = {
                        "player_name": player_name,
                        "market": market,
                        "prop_line": prop_line,
                        "bookmaker_odds": matching_odds
                    }

                    if bookmaker == "underdog":
                        underdog_props.append(player_entry)
                    elif bookmaker == "prizepicks":
                        prizepicks_props.append(player_entry)

        underdog_props = filter_better_odds_lean(underdog_props, "ud")
        prizepicks_props = filter_better_odds_lean(prizepicks_props, "pp")

        return JsonResponse({
            "underdog_props": underdog_props,
            "prizepicks_props": prizepicks_props
        }, safe=False)

    except Exception as e:
        print("Error:", e)  # Debugging line
        return JsonResponse({"error": str(e)}, safe=False)