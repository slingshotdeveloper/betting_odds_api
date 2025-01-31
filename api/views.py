from django.http import JsonResponse
from django.views import View
import requests
import json
from openpyxl.utils.dataframe import dataframe_to_rows
import pandas as pd
from .services.nba.nba_events import get_nba_events
from .services.nba.nba_player_props_odds import get_nba_player_props_odds
from .services.nba.nba_dfs_player_prop_lines import get_dfs_player_props_lines

class HomeView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({"message": "Hello, World!"})

def get_nba_player_props_value(request, event_id):
    """
    Combine player point props from NBA bookmakers with DFS lines from underdog and prizepicks.
    Filters out bookmaker odds that don't match the DFS point line.
    """
    
    try:
        # Fetch player prop odds from NBA bookmakers
        player_props_odds = get_nba_player_props_odds(request, event_id).get("player_props", {})
        
        # Fetch player prop lines from Underdog and PrizePicks
        underdog_prizepicks_data = get_dfs_player_props_lines(request, event_id).get("player_props", {})        

        combined_player_props = {}

        # Loop through each player from the DFS sites data
        for player_name, dfs_lines in underdog_prizepicks_data.items():
            if player_name not in player_props_odds:
                continue  # Skip players that don't exist in the NBA bookmaker data

            # Separate the DFS lines into underdog and prizepicks
            underdog_lines = []
            prizepicks_lines = []

            for dfs_line in dfs_lines:
                prop_line = dfs_line["prop_line"]
                market = dfs_line["market"]

                # Filter matching bookmaker odds based on the point line for both underdog and prizepicks
                matching_bookmaker_odds = [
                    bookmaker for bookmaker in player_props_odds.get(player_name, [])
                    if bookmaker["point"] == prop_line and bookmaker["market"] == market
                ]

                # If there are matching odds, append to the correct DFS site list
                if matching_bookmaker_odds:
                    if dfs_line["bookmaker"].lower() == "underdog":
                        underdog_lines.append({
                            market: prop_line,
                            "bookmaker_odds": matching_bookmaker_odds
                        })
                    elif dfs_line["bookmaker"].lower() == "prizepicks":
                        prizepicks_lines.append({
                            market: prop_line,
                            "bookmaker_odds": matching_bookmaker_odds
                        })

            # Only include the player if they have matching lines from either underdog or prizepicks
            if underdog_lines or prizepicks_lines:
                combined_player_props[player_name] = {
                    "underdog": underdog_lines,
                    "prizepicks": prizepicks_lines
                }
    
        return JsonResponse({"player_props": combined_player_props}, safe=False)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)