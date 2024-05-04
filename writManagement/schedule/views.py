from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from datetime import datetime
import json
from .models import departments, meetings
from bson import ObjectId


meeting_info = ['title', 'date', 'startTime', 'endTime' , 'location', 'priority', 'minutesOfMeeting', 'summary']   
meeting_array_info = ['departments', 'groups', 'users']

conversion = {
    'title' :  'meetingSubject',
    'date' : 'scheduleDate',
    'location' : 'scheduledLocation',
    'startTime' : 'scheduledStartTime',
    'endTime' : 'scheduledEndTime',
    'priority' : 'selectedPriority',
    'minutesOfMeeting' : 'minutesOfMeeting',
    'summary' : 'summary',
    'departments': 'departments',
    'groups' : 'groups', 
    'users' : 'users' 
}


#return all the meetings that are under the user
@require_http_methods(["GET"])
def get_meetings(request):
    try :
        # allMeetings = meetings.find({'users' : request.user.id})
        allMeetings = meetings.find({})
        events = []
        for meet in allMeetings:
            currentMeet = {}
            currentMeet['_id'] = str(meet['_id'])
            for info in meeting_info:
                if conversion[info] in meet:
                    currentMeet[info] = meet[conversion[info]]
                else:
                    currentMeet[info] = ""
            for info in meeting_array_info:
                if conversion[info] in meet:
                    currentMeet[info] = meet[conversion[info]]
                else:
                    currentMeet[info] = []
                    
            events.append(currentMeet)
            # print("Hemang" , events)
            
        return JsonResponse({'success':True, 'data' : events})
        
    except Exception as e:
        return JsonResponse({'success' : False, 'error' : e})
    
    
    # events = [
    #     {
    #         'id': 1,
    #         'title': 'Meeting 111',
    #         'start': datetime(2024, 3, 10, 4, 0), 
    #         'end': datetime(2024, 3, 10, 6, 0),   
    #         'location': 'DC Office',
    #         'priority': 'high',
    #         'departments': ['Marketing', 'Development', 'HR'],
    #         'groups': ['Group 1', 'Group 2'],
    #         'users': ['User 1', 'User 2'],
    #         'minutesOfMeeting': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
    #         'summary': 'Meeting went well. Discussed project milestones and assigned tasks.',
    #     },
    #     {
    #         'id': 3,
    #         'title': 'Meeting 3',
    #         'start': datetime(2024, 3, 10, 10, 0), 
    #         'end': datetime(2024, 3, 10, 12, 0),   
    #         'location': 'DC Office',
    #         'priority': 'medium',
    #         'departments': ['Marketing', 'Development', 'HR'],
    #         'groups': ['Group 3'],
    #         'users': ['User 1', 'User 2'],
    #         'minutesOfMeeting': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
    #         'summary': 'Meeting went well. Discussed project milestones and assigned tasks.',
    #     },
    #     {
    #         'id': 2,
    #         'title': 'Meeting 2',
    #         'start': datetime(2024, 3, 25, 14, 0), 
    #         'end': datetime(2024, 3, 25, 16, 0),    
    #         'location': 'DC Office',
    #         'priority': 'low',
    #         'departments': ['Marketing', 'Development', 'HR'],
    #         'groups': ['Group 2'],
    #         'users': ['User 1', 'User 2'],
    #         'minutesOfMeeting': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
    #         'summary': 'Meeting went well. Discussed project milestones and assigned tasks.',
    #     },
    # ]


@require_http_methods(["POST"])
def create_new_meeting(request):
    try:
        data = json.loads(request.body)
        scheduleDate = datetime.strptime(data['scheduleDate'], '%Y-%m-%d')
        scheduledStartTime = datetime.strptime(data['scheduledStartTime'], '%H:%M')
        scheduledEndTime = datetime.strptime(data['scheduledEndTime'], '%H:%M')
        meeting_data = {
            'meetingSubject': data['meetingSubject'],
            'scheduleDate': scheduleDate,
            'scheduledLocation': data['scheduledLocation'],
            'scheduledStartTime': scheduledStartTime,
            'scheduledEndTime': scheduledEndTime,
            'selectedPriority': data['selectedPriority']['key'],
            'minutesOfMeeting' : "",
            'summary' : "",
            'departments' : [],
            'groups' : [],
            'users' : []
        }
        meetings.insert_one(meeting_data)
        print(meeting_data)
        return JsonResponse({'success': True, 'message': 'successfully created meeting'})
    except Exception as e:
        return JsonResponse({'success' : False, 'error' : e})

@require_http_methods(["POST"])
def add_department(request):
    try:
        data = json.loads(request.body)
        departments.insert_one(data)
        # print("----------")
        print(data)
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': e})
    

@require_http_methods(["GET"])
def get_departments(request):
    try:
        all_departments = departments.find({})
        data = []
        for x in all_departments:
            temp = {}
            temp['_id'] = str(x['_id'])
            temp['departmentName'] = x['departmentName']
            temp['departmentDescription'] = x['departmentDescription']
            temp['departmentUsers'] = x['departmentUsers']
            data.append(temp)
        # print(data)
        return JsonResponse({'success': True, 'data' : data})
    except Exception as e:
        return JsonResponse({'success': False, 'error': e})
    
@require_http_methods(["POST"])
def delete_department(request):
    try:
        object_id = json.loads(request.body)
        print(object_id)
        if object_id:
            result = departments.delete_one({'_id': ObjectId(object_id)})
            if result.deleted_count == 1:
                return JsonResponse({'success': True, 'message': 'Department Deleted Successfully'})
            else:
                return JsonResponse({'success': False, 'message': 'Department not found or already deleted'})
        else:
            return JsonResponse({'success': False, 'message': 'Object ID not provided'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': e})

@require_http_methods(["POST"])
def update_department(request):
    try:
        data = json.loads(request.body)
        department_id = data.get('_id')
        print(data)
        if department_id:
            result = departments.update_one(
                {'_id': ObjectId(department_id)},
                {'$set': {'departmentName': data['departmentName'], 'departmentDescription': data['departmentDescription'], 'departmentUsers' : data['departmentUsers']}}
            )
            if result.modified_count == 1: 
                return JsonResponse({'success': True, 'message': 'Department Updated Successfully'})
            else:
                return JsonResponse({'success': False, 'message': 'Department not found or no changes made'})
        else:
            return JsonResponse({'success': False, 'message': 'Object ID not provided'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': e})
    
@require_http_methods(["POST"])
def delete_meeting(request):
    try:
        data = json.loads(request.body)
        _id = data.get('_id')
        print(_id)
        result = meetings.delete_one({'_id': ObjectId(_id)})

        # Check if the document was deleted successfully
        if result.deleted_count == 1:
            return JsonResponse({'success': True, 'message': 'Meeting deleted successfully'})
        else:
            return JsonResponse({'success': False, 'message': 'Meeting not found or not deleted'})

    except Exception as e:
        return JsonResponse({'success': False, 'message': 'Meeting not found or not deleted' + e})

@require_http_methods(["POST"])
def update_meeting(request):
    try:
        data = json.loads(request.body)
        meeting_id = data.get('_id')
        scheduleDate = datetime.strptime(data['scheduleDate'], '%Y-%m-%d')
        scheduledStartTime = datetime.strptime(data['scheduledStartTime'], '%H:%M')
        scheduledEndTime = datetime.strptime(data['scheduledEndTime'], '%H:%M')
        meeting_data = {
            'meetingSubject': data['meetingSubject'],
            'scheduleDate': scheduleDate,
            'scheduledLocation': data['scheduledLocation'],
            'scheduledStartTime': scheduledStartTime,
            'scheduledEndTime': scheduledEndTime,
            # 'selectedPriority': data['selectedPriority']['key'],
            'minutesOfMeeting' : data['meetingMinutes'],
            'summary' : data['meetingSummary'],
        }
        print(data)
        update_data = {}
        for key, value in data.items():
            if key in conversion:
                update_data[conversion[key]] = value
        result = meetings.update_one(
            {'_id': ObjectId(meeting_id)},
            {'$set': meeting_data}
        )
        if result:
            return JsonResponse({'success': True, 'message': 'Meeting updated successfully'})
        else :
            return JsonResponse({'success': False, 'message': "Meeting not found"})
    except Exception as e:
        print("update_meeting Not working")
        return JsonResponse({'success': False, 'message': 'Meeting not found or not updated' + e})
    
    
@require_http_methods(['POST'])
def searchInMeeting(request):
    try: 
        data = json.loads(request.body)
        searchText = data.get('searchText')
        searchText = searchText.strip()
        if searchText == "":
            return JsonResponse({'success' : True, 'data' : []})
        searchFilter = [{"$text": {"$search": searchText}}]
        result = meetings.find(searchFilter)
        return JsonResponse({'success' : True, 'data' : result})
    except Exception as err:
        return JsonResponse({'success': False, 'error' : err, 'message' : 'Some error occured!'})

