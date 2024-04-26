from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from datetime import datetime
import json
from .models import departments


@require_http_methods(["GET"])
def get_all_departments(request):
    departments = [
        {'departmentId': 1, 'departmentName': 'Department A', 'departmentDescription': 'Description for Department A', 'departmentUsers': ['Hemang', 'Deepanshu']},
        {'departmentId': 2, 'departmentName': 'Department B', 'departmentDescription': 'Description for Department B', 'departmentUsers': ['Hemang', 'Rajat']},
        {'departmentId': 3, 'departmentName': 'Department C', 'departmentDescription': 'Description for Department C', 'departmentUsers': ['Rajat', 'Ankush']},
    ]
    return JsonResponse({'success': True, 'data': departments})


@require_http_methods(["GET"])
def get_meetings(request):
    events = [
        {
          'id': 1,
          'title': 'Meeting 111',
          'start': datetime(2024, 3, 10, 4, 0), 
          'end': datetime(2024, 3, 10, 6, 0),   
          'location': 'DC Office',
          'priority': 'high',
          'departments': ['Marketing', 'Development', 'HR'],
          'groups': ['Group 1', 'Group 2'],
          'users': ['User 1', 'User 2'],
          'minutesOfMeeting': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
          'summary': 'Meeting went well. Discussed project milestones and assigned tasks.',
        },
        {
          'id': 3,
          'title': 'Meeting 3',
          'start': datetime(2024, 3, 10, 10, 0), 
          'end': datetime(2024, 3, 10, 12, 0),   
          'location': 'DC Office',
          'priority': 'medium',
          'departments': ['Marketing', 'Development', 'HR'],
          'groups': ['Group 3'],
          'users': ['User 1', 'User 2'],
          'minutesOfMeeting': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
          'summary': 'Meeting went well. Discussed project milestones and assigned tasks.',
        },
        {
          'id': 2,
          'title': 'Meeting 2',
          'start': datetime(2024, 3, 25, 14, 0), 
          'end': datetime(2024, 3, 25, 16, 0),    
          'location': 'DC Office',
          'priority': 'low',
          'departments': ['Marketing', 'Development', 'HR'],
          'groups': ['Group 2'],
          'users': ['User 1', 'User 2'],
          'minutesOfMeeting': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
          'summary': 'Meeting went well. Discussed project milestones and assigned tasks.',
        },
    ]
    return JsonResponse({'success': True, 'data': events})


@require_http_methods(["POST"])
def hemang(request):
    data = json.loads(request.body)
    print(data)
    return JsonResponse({'success': True})

@require_http_methods(["POST"])
def add_department(request):
    try:
        data = json.loads(request.body)
        departments.insert_one(data)
        print(data)
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': e})
    
@require_http_methods({"GET"})
def get_departments(request):
    try:
        all_departments = departments.find({})
        print(all_departments)
        return JsonResponse({'success': True, 'data' : all_departments})
    except Exception as e:
        return JsonResponse({'success': False, 'error': e})