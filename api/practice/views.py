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

def getRecentChippingCalibrations(request):
    drills = PracticeGame.objects.filter(game_type='chipping_calibration').order_by('-date')[:10]
    results = []
    for drill in drills:
        deserialized_drill_data = json.loads(drill.game_data)
        ground_strike_successes = deserialized_drill_data['groundStrikeValues'].count('Good')
        face_strike_successes = deserialized_drill_data['faceStrikeValues'].count('Sweet spot')
        distance_successes = deserialized_drill_data['distanceValues'].count('Good')
        direction_successes = deserialized_drill_data['directionValues'].count('Within Target Area')

        results.append({
            'date': drill.date,
            'ground_strike_successes': ground_strike_successes,
            'face_strike_successes': face_strike_successes,
            'distance_successes': distance_successes,
            'direction_successes': direction_successes
        })

    return JsonResponse(results, safe=False)

def getRecentPuttingCalibrations(request):
    drills = PracticeGame.objects.filter(game_type='putting_calibration').order_by('-date')[:10]
    results = []
    for drill in drills:
        deserialized_drill_data = json.loads(drill.game_data)
        distance_control_values = deserialized_drill_data['distanceControlValues']
        hole_side_values = deserialized_drill_data['holeSideValues']

        distance_control_successes = distance_control_values.count('Good')
        hole_side_high = hole_side_values.count('High')
        hole_side_low = hole_side_values.count('Low')
        number_holed = hole_side_values.count('Holed')

        results.append({
            'date': drill.date,
            'distance_control_successes': distance_control_successes,
            'hole_side_high': hole_side_high,
            'hole_side_low': hole_side_low,
            'number_holed': number_holed
        })

    return JsonResponse(results, safe=False)


def getRecentDifferentialSessions(request):
    drills = PracticeGame.objects.filter(game_type='differential').order_by('-date')[:10]
    results = []
    for drill in drills:
        deserialized_drill_data = json.loads(drill.game_data)
        results.append({
            'date': drill.date,
            'num_toes': deserialized_drill_data['toes'].count(True),
            'num_heels': deserialized_drill_data['heels'].count(True),
            'num_sweet_spots': deserialized_drill_data['sweetSpots'].count(True),
            'num_tops': deserialized_drill_data['tops'].count(True),
            'num_thins': deserialized_drill_data['thins'].count(True),
            'num_fats': deserialized_drill_data['fats'].count(True),
            'num_good_strikes': deserialized_drill_data['goodStrikes'].count(True),
            'num_draws': deserialized_drill_data['draws'].count(True),
            'num_fades': deserialized_drill_data['fades'].count(True),
            'num_straight': deserialized_drill_data['straight'].count(True),
        })

    return JsonResponse(results, safe=False)
