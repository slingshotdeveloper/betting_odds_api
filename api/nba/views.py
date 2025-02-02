from django.http import JsonResponse
from django.views import View
import requests
import json
from openpyxl.utils.dataframe import dataframe_to_rows
import pandas as pd
from .services.nba_events import get_nba_events
from .services.nba_player_props_odds import get_nba_player_props_odds
from .services.nba_dfs_player_prop_lines import get_dfs_player_props_lines
from .utils import *

class HomeView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({"message": "Hello, World!"})

def get_nba_player_props_value(request, event_id):
    """
    Combine player point props from NBA bookmakers with DFS lines from Underdog and PrizePicks.
    Filters out bookmaker odds that don't match the DFS point line.
    """

    try:
        event_ids = get_nba_events(request)
        selected_event_ids = [event_ids[5]]  # Process only the first event for now

        combined_player_props = {"underdog": {}, "prizepicks": {}}
        underdog_props = []  # Array for all Underdog props
        prizepicks_props = []  # Array for all PrizePicks props
        for event_id in selected_event_ids:
            # Fetch player prop odds from NBA bookmakers
            player_props_odds = get_nba_player_props_odds(request, event_id).get("player_props", {})
            # Fetch player prop lines from Underdog and PrizePicks
            underdog_prizepicks_data = get_dfs_player_props_lines(request, event_id).get("player_props", {})

            for player_name, dfs_lines in underdog_prizepicks_data.items():
                if player_name not in player_props_odds:
                    continue  # Skip players that don't exist in the NBA bookmaker data

                for dfs_line in dfs_lines:
                    prop_line = dfs_line["prop_line"]
                    market = dfs_line["market"]
                    bookmaker = dfs_line["bookmaker"].lower()  # Normalize bookmaker name

                    # Filter matching bookmaker odds based on the point line for both Underdog and PrizePicks
                    matching_bookmaker_odds = [
                        bookmaker for bookmaker in player_props_odds.get(player_name, [])
                        if bookmaker["point"] == prop_line and bookmaker["market"] == market
                    ]

                    if matching_bookmaker_odds:
                        # Initialize player entry if it doesn't exist
                        if player_name not in combined_player_props[bookmaker]:
                            combined_player_props[bookmaker][player_name] = []

                        player_entry = {
                            "player_name": player_name,
                            "market": market,
                            "prop_line": prop_line,
                            "bookmaker_odds": matching_bookmaker_odds
                        }

                        # Append the matched data
                        combined_player_props[bookmaker][player_name].append({
                            "market": market,
                            "prop_line": prop_line,
                            "bookmaker_odds": matching_bookmaker_odds
                        })

                        if bookmaker == "underdog":
                            underdog_props.append(player_entry)
                        elif bookmaker == "prizepicks":
                            prizepicks_props.append(player_entry)

        underdog_props = filter_better_odds_selection(underdog_props)
        prizepicks_props = filter_better_odds_selection(prizepicks_props)

        return JsonResponse({"underdog_props": underdog_props, "prizepicks_props": prizepicks_props}, safe=False)

    except Exception as e:
        print("Error:", e)  # Debugging line
        return JsonResponse({"error": str(e)}, safe=False)