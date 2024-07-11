from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import PracticeStroke, PracticeGame

@csrf_exempt
def savePracticeStroke(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            stroke = PracticeStroke()
            for key, value in data.items():
                setattr(stroke, key, value)
            
            stroke.save()
            
            return JsonResponse({'message': 'Data saved successfully'})
        except Course.DoesNotExist:
            return JsonResponse({'error': 'Course not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)


@csrf_exempt
def savePracticeGame(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            game = PracticeGame()
            for key, value in data.items():
                setattr(game, key, value)
            
            stroke.save()
            
            return JsonResponse({'message': 'Data saved successfully'})
        except Course.DoesNotExist:
            return JsonResponse({'error': 'Course not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
