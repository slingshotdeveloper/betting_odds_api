from django.urls import path
from .nba.views import HomeView, get_nba_events_info, get_nba_player_props_value
from .nfl.views import get_nfl_events_info, get_nfl_player_props_value
from .mlb.views import get_mlb_events_info, get_mlb_player_props_value
from .nhl.views import get_nhl_events_info, get_nhl_player_props_value
from .ncaaf.views import get_ncaaf_events_info, get_ncaaf_player_props_value
from .ncaab.views import get_ncaab_events_info, get_ncaab_player_props_value

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    #nba
    path("nba/events", get_nba_events_info, name="nba_events"),
    path("nba/dfs-player-props", get_nba_player_props_value, name="nba_player_props_value"),
    #nfl
    path("nfl/events", get_nfl_events_info, name="nfl_events"),
    path("nfl/dfs-player-props", get_nfl_player_props_value, name="nfl_player_props_value"),
    #mlb
    path("mlb/events", get_mlb_events_info, name="mlb_events"),
    path("mlb/dfs-player-props", get_mlb_player_props_value, name="mlb_player_props_value"),
    #nhl
    path("nhl/events", get_nhl_events_info, name="nhl_events"),
    path("nhl/dfs-player-props", get_nhl_player_props_value, name="nhl_player_props_value"),
    #ncaaf
    path("ncaaf/events", get_ncaaf_events_info, name="ncaaf_events"),
    path("ncaaf/dfs-player-props", get_ncaaf_player_props_value, name="ncaaf_player_props_value"),
    #ncaab
    path("ncaab/events", get_ncaab_events_info, name="ncaab_events"),
    path("ncaab/dfs-player-props", get_ncaab_player_props_value, name="ncaab_player_props_value"),
]
