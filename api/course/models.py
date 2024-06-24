from django.db import models

class Course(models.Model):
    name = models.CharField(max_length = 200)
    creation_date = models.DateTimeField('Creation Date')
    address = models.CharField(max_length = 200)
    par = models.IntegerField()
    designer = models.CharField(max_length = 200)
    public = models.BooleanField()
    bound_points = models.JSONField(null = True, blank=True)
    image_url = models.CharField(max_length = 200, null=True)
    num_holes = models.IntegerField()

    def __str__(self):
        return self.name

class Tee(models.Model):
    color =  models.CharField(max_length = 6)
    name = models.CharField(max_length = 200)
    yardage = models.IntegerField(null = True)
    slope = models.IntegerField()
    rating = models.IntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

class Hole(models.Model):
    hole_number = models.IntegerField()
    nickname = models.CharField(max_length = 200, null = True, blank=True)
    par = models.IntegerField()
    bound_points = models.JSONField(null = True, blank=True)
    center_green_point = models.JSONField(null = True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)