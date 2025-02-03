from django.urls import path
from .nba.views import HomeView, get_nba_events_info, get_nba_player_props_value
from .nfl.views import get_nfl_events_info, get_nfl_player_props_value

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("nba/events", get_nba_events_info, name="nba_events"),
    path("nba/dfs-player-props", get_nba_player_props_value, name="nba_player_props_value"),
    path("nfl/events", get_nfl_events_info, name="nfl_events"),
    path("nfl/dfs-player-props", get_nfl_player_props_value, name="nfl_player_props_value"),
]
