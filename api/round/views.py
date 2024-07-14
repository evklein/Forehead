from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Round, HoleStats, Stroke, Putt
from course.models import Course, Hole, Tee

def index(request):
    return HttpResponse("Hello, world. You're at the rounds index.")

def fetchRound(request, round_id):
    round = Round.objects.get(pk=round_id)
    raw_data = serializers.serialize('json', [round], ensure_ascii=False)
    trimmed_data = raw_data[1:-1]
    return HttpResponse(trimmed_data, content_type='application/json')

def fetchRoundsInProgress(request):
    rounds = Round.objects.filter(in_progress=True)
    raw_data = serializers.serialize('json', rounds)
    return HttpResponse(raw_data, content_type='application/json')

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

def fetchRoundHoleStats(request, round_id):
    stats = HoleStats.objects.filter(rnd=round_id)
    raw_data = serializers.serialize('json', stats)
    return HttpResponse(raw_data, content_type='application/json')

def fetchRoundStrokes(request, round_id):
    strokes = Stroke.objects.filter(rnd=round_id)
    raw_data = serializers.serialize('json', strokes)
    return HttpResponse(raw_data, content_type='application/json')

def fetchRoundPutts(request, round_id):
    putts = Putt.objects.filter(rnd=round_id)
    raw_data = serializers.serialize('json', putts)
    return HttpResponse(raw_data, content_type='application/json')

@csrf_exempt
def saveNewRound(request):
    if request.method == 'POST':
        try:
            course_id = request.GET.get('course_id', -1)
            print("COURSE ID")
            print(course_id)
            course = Course.objects.get(pk=course_id)
            tee_id = request.GET.get('tee_id', -1)
            tee = Tee.objects.get(pk=tee_id)

            data = json.loads(request.body)
            round = Round(course=course, played_tee=tee)
            for key, value in data.items():
                setattr(round, key, value)
            round.in_progress = True
            
            round.save()

            return JsonResponse({'message': 'Data saved successfully', 'round_id': round.id})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

@csrf_exempt
def updateRound(request, round_id):
    if request.method == 'POST':
        try:
            round = Round.objects.get(pk=round_id)
            data = json.loads(request.body)
            for key, value in data.items():
                setattr(round, key, value)
            round.in_progress = True
            
            round.save()

            return JsonResponse({'message': 'Data saved successfully', 'round_id': round.id})
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
            
            existing_stats = HoleStats.objects.filter(rnd=rnd, hole=hole)
            if existing_stats is not None:
                stats = existing_stats[0]

            for key, value in data.items():
                sanitized_val = value
                if value == 'true':
                    sanitized_val = True
                elif value == 'false':
                    sanitized_val = False
                setattr(stats, key, sanitized_val)
            
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

            existing_strokes = Stroke.objects.filter(rnd=rnd, hole=hole, stroke_number=data['stroke_number'])
            if existing_strokes is not None:
                stroke = existing_strokes[0]

            for key, value in data.items():
                setattr(stroke, key, value)
            
            print(stroke)
            stroke.save()
            print("Stroke saved")

            return JsonResponse({'message': 'Data saved successfully'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import time
from .models import Round, Hole, Putt
from django.db import OperationalError

@csrf_exempt
def savePutt(request, round_id, hole_id):
    if request.method == 'POST':
        try:
            rnd = Round.objects.get(pk=round_id)
            hole = Hole.objects.get(pk=hole_id)
            data = json.loads(request.body)

            retry_attempts = 5
            for attempt in range(retry_attempts):
                try:
                    putt, created = Putt.objects.update_or_create(
                        rnd=rnd, 
                        hole=hole, 
                        stroke_number=data['stroke_number'],
                        defaults=data
                    )
                    return JsonResponse({'message': 'Data saved successfully', 'created': created})
                except OperationalError as e:
                    if 'database is locked' in str(e) and attempt < retry_attempts - 1:
                        time.sleep(2)  # wait for 2 seconds before retrying
                    else:
                        raise

        except Round.DoesNotExist:
            return JsonResponse({'error': 'Round not found'}, status=404)
        except Hole.DoesNotExist:
            return JsonResponse({'error': 'Hole not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
