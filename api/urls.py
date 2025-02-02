from django.urls import path
from .nba import views
from .nba.views import HomeView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("nba/<str:event_id>/", views.get_nba_player_props_value, name="nba_player_props_value")
]
