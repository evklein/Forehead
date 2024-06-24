from django.db import models

from course.models import Course, Tee, Hole

class Round(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_played = models.DateField()
    tee_time = models.CharField(max_length = 50)
    finish_time = models.CharField(max_length = 50)
    holes_completed = models.IntegerField()
    played_tee = models.ForeignKey(Tee, on_delete=models.CASCADE)
    group_makeup = models.CharField(max_length = 50)
    mobility = models.CharField(max_length = 50)
    round_counts_toward_hci = models.BooleanField()
    notes = models.CharField()

class HoleScore(models.Model):
    score = models.IntegerField()
    putts = models.IntegerField()
    gir = models.BooleanField()
    gld = models.BooleanField()
    scrambling = models.BooleanField(null = True)
    rnd = models.ForeignKey(Round, on_delete=models.CASCADE)
    hole = models.ForeignKey(Hole, on_delete=models.CASCADE)

class Stroke(models.Model):
    stroke_number = models.IntegerField()
    club = models.CharField(max_length = 50)
    distance = models.IntegerField()
    start_coordinate = models.JSONField()
    end_coordinate = models.JSONField(null = True)
    hole_score = models.ForeignKey(HoleScore, on_delete=models.CASCADE)

class Putt(models.Model):
    stroke_number = models.IntegerField()
    distance = models.IntegerField()
    hole_score = models.ForeignKey(HoleScore, on_delete=models.CASCADE)

