from django.contrib import admin

from .models import Course
from .models import Tee
from .models import Hole

admin.site.register(Course)
admin.site.register(Tee)
admin.site.register(Hole)