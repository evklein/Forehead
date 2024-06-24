from django.db import models

from course.models import Course, Tee, Hole

class Round(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    tees = models.ForeignKey(Tee, on_delete=models.CASCADE)
    date_played = models.DateField()

class HoleScore(models.Model):
    score = models.IntegerField()
    putts = models.IntegerField()
    gir = models.BooleanField()
    gld = models.BooleanField()
    scrambling = models.BooleanField(null = True)
    rnd = models.ForeignKey(Round, on_delete=models.CASCADE)
    hole = models.ForeignKey(Hole, on_delete=models.CASCADE)

class Stroke(models.Model):
    stroke = models.IntegerField()
    club = models.CharField(max_length = 50)
    distance = models.IntegerField()
    start_coordinate = models.JSONField()
    end_coordinate = models.JSONField(null = True)
    hole_score = models.ForeignKey(HoleScore, on_delete=models.CASCADE)

class Putt(models.Model):
    stroke = models.IntegerField()
    distance = models.IntegerField()
    hole_score = models.ForeignKey(HoleScore, on_delete=models.CASCADE)

