from django.contrib import admin

from .models import Round, HoleStats, Stroke, Putt

admin.site.register(Round)
admin.site.register(HoleStats)
admin.site.register(Stroke)
admin.site.register(Putt)
