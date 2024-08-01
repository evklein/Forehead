from django.urls import path
from . import views

urlpatterns = [
    path("stroke/", views.savePracticeStroke, name="savePracticeStroke"),
    path("game/", views.savePracticeGame, name="savePracticeGame"),
    path("scramble/recent/", views.getRecentGameScores, name="getRecentGameScores"),
    path("calibrations/recent/", views.getRecentCalibrations, name="getRecentCalibrations"),
    path("chipping-calibrations/recent/", views.getRecentChippingCalibrations, name="getRecentChippingCalibrations"),
    path("putting-calibrations/recent/", views.getRecentPuttingCalibrations, name="getRecentPuttingCalibrations"),
    path("differentials/recent/", views.getRecentDifferentialSessions, name="getRecentDifferentialSessions"),
]
