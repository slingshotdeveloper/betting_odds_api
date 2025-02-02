# utils.py
# markets => 
# [ player_points, player_rebounds, player_assists, player_points_rebounds_assists,
# player_points_rebounds, player_points_assists, player_rebounds_assists, player_blocks, player_steals, 
# player_blocks_steals, player_threes, player_turnovers, player_points_q1, player_rebounds_q1, player_assists_q1
# player_field_goals, player_frees_made, player_frees_attempts ]
NBA_PLAYER_MARKETS = "player_points"
# alternate markets => 
# [ player_points_alternate, player_rebounds_alternate, player_assists_alternate, player_blocks_alternate	
# player_steals_alternate, player_turnovers_alternate, player_threes_alternate, player_points_assists_alternate,
# player_points_rebounds_alternate, player_rebounds_assists_alternate, player_points_rebounds_assists_alternate ]
NBA_ALTERNATE_PLAYER_MARKETS = ""
NBA_PLAYER_ODDS_REGIONS = "us"
NBA_PLAYER_DFS_REGIONS = "us_dfs"
NBA_PLAYER_ODDS_FORMAT = "decimal"

def filter_better_odds_selection(player_props):
    """
    Filters out the worse odds for each player by comparing 'over' and 'under' odds for each bookmaker.
    Keeps only the better (more negative) odds per bookmaker, based on the overall best selection.
    """
    filtered_props = []

    for prop in player_props:
        player_name = prop["player_name"]
        market = prop["market"]
        prop_line = prop["prop_line"]
        bookmaker_odds = prop["bookmaker_odds"]

        market = format_market(market.lower())
        
        over_odds_total = 0
        under_odds_total = 0
        over_count = 0
        under_count = 0
        better_selection = ""

        # Organize odds by bookmaker
        for odds_entry in bookmaker_odds:
            selection = odds_entry["selection"].lower()  # "over" or "under"
            odds = odds_entry["odds"]

            # Track sum and count for averaging
            if selection == "over":
                over_odds_total += odds
                over_count += 1
            elif selection == "under":
                under_odds_total += odds
                under_count += 1

        # Calculate average odds, avoid division by zero
        avg_over_odds = over_odds_total / over_count if over_count > 0 else None
        avg_under_odds = under_odds_total / under_count if under_count > 0 else None

        # Round average odds to two decimal places
        avg_over_odds = round(avg_over_odds, 2) if avg_over_odds is not None else None
        avg_under_odds = round(avg_under_odds, 2) if avg_under_odds is not None else None

        # Determine better selection based on averages
        if avg_over_odds and avg_under_odds:
            if avg_over_odds < avg_under_odds:
                better_selection = "over"
            elif avg_over_odds > avg_under_odds:
                better_selection = "under"
            else:
                better_selection = "n/a"
        elif avg_over_odds:  # If there's no under odds, pick over
            better_selection = "over"
        elif avg_under_odds:  # If there's no over odds, pick under
            better_selection = "under"

        if better_selection == "n/a":
            continue
        
        # Filter bookmaker odds for the better selection
        selected_bookmaker_odds = []
        for odds_entry in bookmaker_odds:
            if odds_entry["selection"].lower() == better_selection:
                selected_bookmaker_odds.append({
                    "selection": odds_entry["selection"],
                    "market": market,
                    "point": prop_line,
                    "odds": decimal_to_american(odds_entry["odds"]),
                    "bookmaker": odds_entry["bookmaker"]
                })

        average_odds = decimal_to_american(avg_over_odds) if better_selection == "over" else decimal_to_american(avg_under_odds)

        # Add the filtered prop to the result list
        filtered_props.append({
            "player_name": player_name,
            "market": market,
            "point": prop_line,
            "selection": better_selection,
            "average_odds": average_odds,
            "implied_probability": implied_probability(average_odds),
            "bookmaker_odds": selected_bookmaker_odds
        })

        filtered_props.sort(key=lambda x: x["implied_probability"], reverse=True)

    return filtered_props


def decimal_to_american(decimal_odds):
    if decimal_odds >= 2.0:
        # Positive American odds
        american_odds = (decimal_odds - 1) * 100
    else:
        # Negative American odds
        american_odds = - (100 / (decimal_odds - 1))
    
    return round(american_odds)

def format_market(market):
    switcher = {
        "player_points": "pts",
        "player_rebounds": "rebs",
        "player_assists": "asts",
        "player_points_rebounds_assists": "pra",
        "player_points_rebounds": "p+r",
        "player_points_assists": "p+a",
        "player_rebounds_assists": "r+a",
        "player_blocks": "blks",
        "player_steals": "stls",
        "player_blocks_steals": "blks+stls",
        "player_threes": "threes",
        "player_turnovers": "to",
        "player_points_q1": "pts_q1",
        "player_rebounds_q1": "rebs_q1",
        "player_assists_q1": "asts_q1",
        "player_field_goals": "fg",
        "player_frees_made": "ftm",
        "player_frees_attempts": "fta"
    }
    return switcher.get(market, "unknown")  # Default to "unknown" if market doesn't match any case

def implied_probability(average_odds):
    """
    Calculate the implied probability from the given average odds.
    Works for both positive and negative American odds.
    
    Args:
        average_odds (float): The average odds in American format.
    
    Returns:
        float: The implied probability, as a percentage.
    """
    if average_odds > 0:  # Positive odds
        probability = 100 / (average_odds + 100)
    else:  # Negative odds
        probability = -average_odds / (-average_odds + 100)
    
    return round(probability * 100, 2)  # Return as percentage, rounded to 2 decimal places