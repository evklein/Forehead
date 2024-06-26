from django.contrib import admin

from .models import Round, HoleScore, Stroke, Putt

admin.site.register(Round)
admin.site.register(HoleScore)
admin.site.register(Stroke)
admin.site.register(Putt)
