from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:round_id>/", views.fetchRound, name="fetchRound"),
    path("<int:round_id>/holes/", views.fetchAllHoleStatsForRound, name="fetchAllHoleStatsForRound"),
    path("<int:round_id>/hole/<int:hole_id>/", views.fetchHoleStats, name="fetchHoleStats"),
    path("<int:round_id>/hole/<int:hole_id>/new/", views.saveHoleStats, name="saveHoleStats"),
    path("<int:round_id>/hole/<int:hole_id>/strokes/", views.fetchHoleStrokes, name="fetchHoleStrokes"),
    path("<int:round_id>/hole/<int:hole_id>/strokes/new/", views.saveStroke, name="saveStroke"),
    path("<int:round_id>/hole/<int:hole_id>/putts/", views.fetchHolePutts, name="fetchHolePutts"),
    path("<int:round_id>/hole/<int:hole_id>/putts/new/", views.savePutt, name="savePutt"),
]
