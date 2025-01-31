# utils.py
# markets => 
# [ player_points, player_rebounds, player_assists, player_points_rebounds_assists,
# player_points_rebounds, player_points_assists, player_rebounds_assists, player_blocks, player_steals, 
# player_blocks_steals, player_threes, player_turnovers, player_points_q1, player_rebounds_q1, player_assists_q1
# player_field_goals, player_frees_made, player_frees_attempts ]
NBA_PLAYER_MARKETS = "player_points,player_rebounds"
# alternate markets => 
# [ player_points_alternate, player_rebounds_alternate, player_assists_alternate, player_blocks_alternate	
# player_steals_alternate, player_turnovers_alternate, player_threes_alternate, player_points_assists_alternate,
# player_points_rebounds_alternate, player_rebounds_assists_alternate, player_points_rebounds_assists_alternate ]
NBA_ALTERNATE_PLAYER_MARKETS = ""
NBA_PLAYER_ODDS_REGIONS = "us"
NBA_PLAYER_DFS_REGIONS = "us_dfs"
NBA_PLAYER_ODDS_FORMAT = "american"

def filter_better_odds(player_props):
    """
    Filters out the worse odds for each player by comparing bookmaker and point line.
    Keeps only the better odds (more negative) for each bookmaker and point line pair.
    If odds are the same, removes both.
    Includes the 'selection' field to indicate if it's 'over' or 'under'.
    """
    for player, props in player_props.items():
        # Create a temporary dictionary to store props by bookmaker and point line
        unique_props = {}

        for prop in props:
            bookmaker = prop["bookmaker"]
            point = prop["point"]
            odds = prop["odds"]
            selection = prop["selection"]  # Include 'selection' for "over" or "under"
            key = (bookmaker, point)  # Use (bookmaker, point) as the key

            if key not in unique_props:
                unique_props[key] = []

            unique_props[key].append(prop)

        # Now, go through each group (same bookmaker, same point line)
        filtered_props = []
        for (bookmaker, point), prop_list in unique_props.items():
            if len(prop_list) == 1:
                # If there's only one prop for this bookmaker and point line, keep it
                filtered_props.append(prop_list[0])
            else:
                # Compare odds for this bookmaker and point line pair
                better_prop = None
                for prop in prop_list:
                    if better_prop is None or (prop["odds"] < better_prop["odds"]):
                        better_prop = prop
                # Check if any two props have the same odds
                if all(prop["odds"] == better_prop["odds"] for prop in prop_list):
                    # If all have the same odds, don't keep any of them
                    continue
                elif all(abs(better_prop["odds"] - prop["odds"]) < 15 for prop in prop_list):
                    continue
                else:
                    # Keep the better prop
                    filtered_props.append(better_prop)

        # Update the player's props to the filtered list
        player_props[player] = filtered_props

    return player_props