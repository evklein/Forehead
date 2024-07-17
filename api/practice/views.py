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
            
            game.save()
            
            return JsonResponse({'message': 'Data saved successfully'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

def getRecentGameScores(request):
    games = PracticeGame.objects.filter(game_type='scramble').order_by('-date')[:10]
    results = []
    for game in games:
        deserialized_game_data = json.loads(game.game_data)
        game_chips = [int(chip) for chip in deserialized_game_data['holeChips']]
        game_putts = [int(putt) for putt in deserialized_game_data['holePutts']]
        game_yardages = [int(yardage) for yardage in deserialized_game_data['holeYardages']]

        results.append({
            'date': game.date,
            'totalShots': sum(game_chips) + sum(game_putts),
            'totalYards': sum(game_yardages)
        })

    return JsonResponse(results, safe=False)

def getRecentCalibrations(request):
    drills = PracticeGame.objects.filter(game_type='swing_calibration').order_by('-date')[:10]
    results = []
    for drill in drills:
        deserialized_drill_data = json.loads(drill.game_data)
        ground_strike_successes = deserialized_drill_data['groundStrikeValues'].count('Good')
        face_strike_successes = deserialized_drill_data['faceStrikeValues'].count('Sweet spot')
        direction_successes = deserialized_drill_data['directionValues'].count('Within Target Area')

        results.append({
            'date': drill.date,
            'ground_strike_successes': ground_strike_successes,
            'face_strike_successes': face_strike_successes,
            'direction_successes': direction_successes
        })

    return JsonResponse(results, safe=False)
