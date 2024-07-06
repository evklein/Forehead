from django.db import models

class PracticeStroke(models.Model):
    recorded_time = models.DateTimeField(auto_now_add=True, blank=True)
    shot_type = models.CharField(max_length=50)
    shot_distance = models.IntegerField()
    mis_hit = models.CharField(max_length = 50, null=True, blank=True)
    result_side = models.CharField(max_length=50, null=True, blank=True)
    result_distance = models.CharField(max_length=50, null=True, blank=True)
    result_shape_direction = models.CharField(max_length=50, null=True, blank=True)
    result_shape = models.CharField(max_length=50, null=True, blank=True)

class PracticeGame(models.Model):
    date = models.DateTimeField(auto_now_add=True, blank=True)
    game_type = models.CharField(max_length=50)
    game_data = models.JSONField(null=True, blank=True)
