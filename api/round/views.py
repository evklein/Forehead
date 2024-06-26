from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers

from .models import Round, HoleScore, Stroke, Putt

def index(request):
    return HttpResponse("Hello, world. You're at the rounds index.")

def fetchRound(request, round_id):
    round = Round.objects.get(pk=round_id)
    # include_hole_score_objects = request.GET.get('includeHoleScoreObjs', False)
    raw_data = serializers.serialize('json', [round], ensure_ascii=False)
    trimmed_data = raw_data[1:-1]
    return HttpResponse(trimmed_data, content_type='application/json')

def fetchRoundHoleScores(request, round_id):
    hole_scores = HoleScore.objects.filter(rnd=round_id)
    raw_data = serializers.serialize('json', hole_scores)
    return HttpResponse(raw_data, content_type='application/json')

def fetchHoleScore(request, hole_score_id):
    hole_score = HoleScore.objects.get(pk=hole_score_id)
    raw_data = serializers.serialize('json', [hole_score], ensure_ascii=False)
    trimmed_data = raw_data[1:-1]
    return HttpResponse(trimmed_data, content_type='application/json')

def fetchHoleScoreStrokes(request, hole_score_id):
    strokes = Stroke.objects.filter(hole_score=hole_score_id)
    raw_data = serializers.serialize('json', strokes)
    return HttpResponse(raw_data, content_type='application/json')

def fetchHoleScorePutts(request, hole_score_id):
    putts = Putt.objects.filter(hole_score=hole_score_id)
    raw_data = serializers.serialize('json', putts)
    return HttpResponse(raw_data, content_type='application/json')

def fetchStroke(request, stroke_id):
    stroke = Stroke.objects.get(pk=stroke_id)
    raw_data = serializers.serialize('json', [stroke], ensure_ascii=False)
    trimmed_data = raw_data[1:-1]
    return HttpResponse(trimmed_data, content_type='application/json')

def fetchPutt(request, putt_id):
    putt = Putt.objects.get(pk=putt_id)
    raw_data = serializers.serialize('json', [putt], ensure_ascii=False)
    trimmed_data = raw_data[1:-1]
    return HttpResponse(trimmed_data, content_type='application/json')