from django.urls import path
from . import views

urlpatterns = [
    path("stroke/", views.savePracticeStroke, name="savePracticeStroke"),
]
