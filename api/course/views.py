from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import json



from .models import Course, Hole

@csrf_exempt
def index(request):
    return HttpResponse("Hello, world. You're at the course index.")

def all(request):
    courses = Course.objects.all().order_by('creation_date')
    data = serializers.serialize('json', courses)
    return HttpResponse(data, content_type='application/json')

def details(request, course_id):
    course = Course.objects.get(pk=course_id)
    print(course.name)
    data = serializers.serialize('json', [course], ensure_ascii=False)
    trimmed_data = data[1:-1]
    return HttpResponse(trimmed_data, content_type='application/json')

@csrf_exempt
def save(request, course_id):
    if request.method == 'POST':
        try:
            course = Course.objects.get(pk=course_id)
            
            # Parse the JSON data from the request body
            data = json.loads(request.body)
            
            # Update the course object with the data
            for key, value in data.items():
                setattr(course, key, value)
            
            # Save the updated course object
            course.save()
            
            return JsonResponse({'message': 'Data saved successfully'})
        except Course.DoesNotExist:
            return JsonResponse({'error': 'Course not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

def hole(request, course_id, hole_number):
    course = Course.objects.get(pk=course_id)
    hole = Hole.objects.filter(course=course, hole_number=hole_number)
    data = serializers.serialize('json', hole)
    trimmed_data = data[1:-1]
    return HttpResponse(trimmed_data, content_type='application/json')

@csrf_exempt
def save_hole(request, course_id, hole_number):
    if request.method == 'POST':
        try:
            course = Course.objects.get(pk=course_id)
            hole = Hole.objects.filter(course=course, hole_number=hole_number).first()

            if hole is None:
                hole = Hole(course=course, hole_number=hole_number)
                hole.course = course
            
            data = json.loads(request.body)
            # Parse the JSON data from the request body
            
            # Update the course object with the data
            for key, value in data.items():
                setattr(hole, key, value)
            
            # Save the updated course object
            hole.save()
            
            return JsonResponse({'message': 'Data saved successfully'})
        except Course.DoesNotExist:
            return JsonResponse({'error': 'Course not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)



