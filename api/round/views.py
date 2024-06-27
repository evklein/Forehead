from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers

from .models import Round, HoleStats, Stroke, Putt

def index(request):
    return HttpResponse("Hello, world. You're at the rounds index.")

def fetchRound(request, round_id):
    round = Round.objects.get(pk=round_id)
    # include_hole_score_objects = request.GET.get('includeHoleScoreObjs', False)
    raw_data = serializers.serialize('json', [round], ensure_ascii=False)
    trimmed_data = raw_data[1:-1]
    return HttpResponse(trimmed_data, content_type='application/json')

def fetchAllHoleStatsForRound(request, round_id):
    hole_scores = HoleStats.objects.filter(rnd=round_id)
    raw_data = serializers.serialize('json', hole_scores)
    return HttpResponse(raw_data, content_type='application/json')

def fetchHoleStats(request, round_id, hole_id):
    hole_score = HoleStats.objects.filter(rnd=round_id, hole=hole_id).first()
    raw_data = serializers.serialize('json', [hole_score], ensure_ascii=False)
    trimmed_data = raw_data[1:-1]
    return HttpResponse(trimmed_data, content_type='application/json')

def fetchHoleStrokes(request, round_id, hole_id):
    strokes = Stroke.objects.filter(hole_score=hole_score_id)
    raw_data = serializers.serialize('json', strokes)
    return HttpResponse(raw_data, content_type='application/json')

def fetchHolePutts(request, round_id, hole_id):
    putts = Putt.objects.filter(hole_score=hole_score_id)
    raw_data = serializers.serialize('json', putts)
    return HttpResponse(raw_data, content_type='application/json')
