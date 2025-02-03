from django.urls import path
from .nba import views
from .nba.views import HomeView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("nba/events", views.get_nba_events_info, name="nba_events"),
    path("nba/dfs-player-props", views.get_nba_player_props_value, name="nba_player_props_value")
]
