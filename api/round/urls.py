from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:round_id>/", views.fetchRound, name="fetchRound"),
    path("<int:round_id>/holes/", views.fetchAllHoleStatsForRound, name="fetchAllHoleStatsForRound"),
    path("<int:round_id>/hole/<int:hole_id>/", views.fetchHoleStats, name="fetchHoleStats"),
    path("<int:round_id>/hole/<int:hole_id>/strokes/", views.fetchHoleStrokes, name="fetchHoleStrokes"),
    path("<int:round_id>/hole/<int:hole_id>/putts/", views.fetchHolePutts, name="fetchHolePutts"),
]
