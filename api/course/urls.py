from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("all/", views.all, name="all"),
    path("<int:course_id>/tees/", views.get_tees, name="tees"),
    path("<int:course_id>/details/", views.details, name="details"),
    path("<int:course_id>/save/", views.save, name="save"),
    path("<int:course_id>/holes/", views.holes, name="holes"),
    path("<int:course_id>/hole/<int:hole_number>", views.hole, name="hole"),
    path("<int:course_id>/hole/<int:hole_number>/save/", views.save_hole, name="saveHole")
]
