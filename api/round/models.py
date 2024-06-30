from django.db import models

from course.models import Course, Tee, Hole

class Round(models.Model):
    nickname = models.CharField(max_length = 200, null=True, blank=True)
    date_played = models.DateField()
    tee_time = models.CharField(max_length = 50, null=True, blank=True)
    finish_time = models.CharField(max_length = 50, null=True, blank=True)
    holes_completed = models.IntegerField()
    group_makeup = models.CharField(max_length = 50, null=True, blank=True)
    mobility = models.CharField(max_length = 50, null=True, blank=True)
    round_counts_toward_hci = models.BooleanField()
    notes = models.CharField(max_length = 5000, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    played_tee = models.ForeignKey(Tee, on_delete=models.CASCADE)

class HoleStats(models.Model):
    gir = models.BooleanField()
    gld = models.BooleanField()
    scrambling = models.BooleanField(null = True)
    rnd = models.ForeignKey(Round, on_delete=models.CASCADE)
    hole = models.ForeignKey(Hole, on_delete=models.CASCADE)

class Stroke(models.Model):
    stroke_number = models.IntegerField()
    club = models.CharField(max_length = 50)
    start_coordinate = models.JSONField(null = True)
    end_coordinate = models.JSONField(null = True)
    penalty = models.BooleanField()
    rnd = models.ForeignKey(Round, on_delete=models.CASCADE)
    hole = models.ForeignKey(Hole, on_delete=models.CASCADE)

class Putt(models.Model):
    stroke_number = models.IntegerField()
    distance = models.IntegerField()
    rnd = models.ForeignKey(Round, on_delete=models.CASCADE)
    hole = models.ForeignKey(Hole, on_delete=models.CASCADE)
