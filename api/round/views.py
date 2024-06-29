from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Round, HoleStats, Stroke, Putt
from course.models import Hole

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

@csrf_exempt
def saveRound(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            round = Round()
            for key, value in data.items():
                setattr(round, key, value)
            
            round.save()

            return JsonResponse({'message': 'Data saved successfully'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

@csrf_exempt
def saveHoleStats(request, round_id, hole_id):
    if request.method == 'POST':
        try:
            rnd = Round.objects.get(pk=round_id)
            hole = Hole.objects.get(pk=hole_id)
            data = json.loads(request.body)
            stats = HoleStats(rnd=rnd, hole=hole)
            for key, value in data.items():
                setattr(stats, key, value)
            
            stats.save()

            return JsonResponse({'message': 'Data saved successfully'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

@csrf_exempt
def saveStroke(request, round_id, hole_id):
    if request.method == 'POST':
        try:
            rnd = Round.objects.get(pk=round_id)
            hole = Hole.objects.get(pk=hole_id)
            data = json.loads(request.body)
            stroke = Stroke(rnd=rnd, hole=hole)
            for key, value in data.items():
                setattr(stroke, key, value)
            
            stroke.save()

            return JsonResponse({'message': 'Data saved successfully'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

@csrf_exempt
def savePutt(request, round_id, hole_id):
    if request.method == 'POST':
        try:
            rnd = Round.objects.get(pk=round_id)
            hole = Hole.objects.get(pk=hole_id)
            data = json.loads(request.body)
            putt = Putt(rnd=rnd, hole=hole)
            for key, value in data.items():
                setattr(putt, key, value)
            
            putt.save()

            return JsonResponse({'message': 'Data saved successfully'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
