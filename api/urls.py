from django.urls import path
from .nba.views import HomeView, get_nba_events_info, get_nba_player_props_value
from .nfl.views import get_nfl_events_info, get_nfl_player_props_value
from .mlb.views import get_mlb_events_info, get_mlb_player_props_value

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
]
