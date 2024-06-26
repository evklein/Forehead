from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:round_id>/", views.fetchRound, name="fetchRound"),
    path("<int:round_id>/hole-scores/", views.fetchRoundHoleScores, name="fetchRoundHoleScores"),

    path("hole-score/<int:hole_score_id>/", views.fetchHoleScore, name="fetchHoleScore"),
    path("hole-score/<int:hole_score_id>/strokes/", views.fetchHoleScoreStrokes, name="fetchHoleScoreStrokes"),
    path("hole-score/<int:hole_score_id>/putts/", views.fetchHoleScorePutts, name="fetchHoleScorePutts"),

    path("stroke/<int:stroke_id>/", views.fetchStroke, name="fetchStroke"),
    
    path("putt/<int:putt_id>/", views.fetchPutt, name="fetchPutt")
]
