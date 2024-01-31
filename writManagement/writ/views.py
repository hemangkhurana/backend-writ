from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
import pymongo
import json
from datetime import datetime
from .mongodb_connection import writs, gridFSWrit
from .models import data 
import base64
from bson import ObjectId
from django.http import HttpResponse
from datetime import datetime

# Create your views here.

writCheck = [
        'writNumber', 'writDate', 'writPetitionerName', 'writRespondentNames', 
        'writDepartment', 'writPetitionerPrayer', 'writCourtOrder', 'writDcComments',
        'writPriority', 'remarkDate', 'paraRemark', 'remarkDcComments', 'contemptDate',
        'contemptText', 'contemptDcComments', 'writDepartment', 'writCloseDate', 'writClose'
    ]

matrix = {
        'column1' : 'writNumber',
        'column2' : 'writPriority',
        'column3' : 'writPetitionerName',
        'column4' :  'writRespondentNames',
        'column5' :  'writDate'
    }

attachments = {'writFileAttachment', 'remarkFileAttachment', 'contemptFileAttachment'}

tempFilterDateList = [None, None, [], [], None, None]
tempMaxValue = [0,0,0,0,0,0]

convertToIndex = {'first' : 0, 'second' : 1, 'third' : 2, 'fourth' : 3, 'fifth' : 4, 'sixth' : 5}


@require_http_methods(['POST'])
def addNewWrit(request):
    try:    
        writNumber = request.POST['writNumber']
        oldWrit = writs.find_one({"writNumber" : writNumber})
        
        if oldWrit:
            for key in request.POST:            
                if key not in writCheck or request.POST[key] == None:   
                    continue
                if key == 'writCloseDate':
                    if request.POST['writClose'] == 'true':
                        oldWrit[key] = request.POST[key]
                else:        
                    oldWrit[key] = request.POST[key]
                
            for attach in attachments:
                if attach in request.FILES:
                    if attach in oldWrit and oldWrit[attach] !='':     
                        gridFSWrit.delete(oldWrit[attach])
                    if str(request.FILES.get(attach)) != '':
                        file = request.FILES.get(attach)
                        file_id = gridFSWrit.put(file.read(), filename=file.name)
                        oldWrit[attach] = str(file_id)
            
            
            #### add what will happen if data is empty, need to update the filters ######
            if request.POST['work'] == 'first':
                oldWrit['filterDateList'][0] = datetime.strptime( request.POST['writDate'], '%Y-%m-%d') 
                oldWrit['writMaxValue'][5-0] = 1
            elif request.POST['work'] == 'second':
                oldWrit['filterDateList'][1] = datetime.strptime( request.POST['remarkDate'], '%Y-%m-%d') 
                oldWrit['writMaxValue'][5-1] = 1
            elif request.POST['work'] == 'fifth':
                oldWrit['filterDateList'][4] = datetime.strptime( request.POST['contemptDate'], '%Y-%m-%d') 
                oldWrit['writMaxValue'][5-4] = 1
            elif request.POST['work'] == 'sixth' and request.POST['writClose']=='true' :
                # do simething
                oldWrit['filterDateList'][5] = datetime.strptime( request.POST['writCloseDate'], '%Y-%m-%d') 
                oldWrit['writMaxValue'][5-5] = 1
                
            writs.replace_one({"writNumber" : writNumber}, oldWrit)
            print(oldWrit)
            
        else:
            writData = {}
            data = request.POST
            
            ###### make sure that update button is available iff there is some input in frontend ####
            # if data == {}:
            #     return JsonResponse({'success' : True, 'Message' : 'Nothing to be updated'})
            for key in data:
                if key in writCheck:
                    writData[key] = data[key]
            
            for attach in attachments:
                if attach in request.FILES:
                    file = request.FILES.get(attach)
                    file_id = gridFSWrit.put(file.read(), filename=file.name)
                    writData['writFileAttachment'] = str(file_id) 
            
            tempFilterDate = tempFilterDateList.copy()
            if 'writDate' in data:
                tempFilterDate[0] = datetime.strptime( data['writDate'], '%Y-%m-%d')
            writData['filterDateList'] = tempFilterDate
            
            writMaxValue = tempMaxValue.copy()
            writMaxValue[5-0] = 1
            writData['writMaxValue'] = writMaxValue
            
            print(writData)
            writs.insert_one(writData)
            
        return JsonResponse({'success' : True})
    except Exception as err:
        return JsonResponse({'success':False,'error' : err})

    
@require_http_methods(['POST'])
def getWrit(request):
    writNumber = json.loads(request.body).get('writNumber',None)
    result = writs.find_one({'writNumber' : writNumber})
    print(result)
    if result is not None:
        temp = {}
        for x in result:
            if x!='_id':
                temp[x] = result[x]
            else:
                temp[x] = str(result[x])
        
        return JsonResponse({'success' : True, 'data' : temp})
    
    else:
        return JsonResponse({'success': False, 'error' : 'Writ not found'})
    
@require_http_methods(['GET'])
def getLatestWrit(request):
    info = writs.find().sort('WritDate',-1).limit(20)
    info = writs.find().sort('WritDate',-1).limit(20)
    data = []
    i = 1
    for x in info:
        temp = {}
        temp['id'] = i
        i+=1
        for col in matrix:
            if matrix[col] in x:
                temp[col] = x[matrix[col]]
        data.append(temp)
    return JsonResponse({'success' : True, 'data' : data})


@require_http_methods(['POST'])
def filterWrit(request):
    oldPostData = json.loads(request.body)
    writFilter = []
    
    filterDates = {}
    for x in oldPostData:
        if x is None or oldPostData[x] == '':
            continue
        
        if x == 'searchText':
            searchText = oldPostData[x]
            searchText = searchText.strip()
            if searchText != '':
                writFilter.append({"$text": {"$search": searchText}})
                
        else:
            y = x[6:]
            y = y[0].lower() + y[1:]
            if (y == 'writRespondentNames' or y == 'writPriority'):
                writFilter.append({y : {"$regex": oldPostData[x], "$options": "i"} }) 
            elif x == 'filterStatus':
                query = {
                    '$expr': {
                        '$cond': {
                            'if': {'$lte': [{'$indexOfArray': ['$writMaxValue', 1]}, 5-oldPostData[x]]},
                            'then': True,
                            'else': False
                        }
                    }
                }
                writFilter.append(query)
            else:
                if x == 'filterEndDate' or x == 'filterStartDate':
                    filterDates[x] = oldPostData[x]
        
    dateQuery = {}
    if len(filterDates) == 2:
        startDate = datetime.strptime(filterDates['filterStartDate'], '%Y-%m-%d')
        endDate =  datetime.strptime(filterDates['filterEndDate'], '%Y-%m-%d')
        dateQuery = {
                '$or': [
                    {'filterDateList': {'$elemMatch': {'$gte': startDate, '$lte': endDate}}},
                    {'filterDateList.2': {'$elemMatch': {'$gte': startDate, '$lte': endDate}}},
                    {'filterDateList.3': {'$elemMatch': {'$gte': startDate, '$lte': endDate}}}
                ]
            }
    
    if len(filterDates) == 1:
        if 'filterStartDate' in filterDates:
            startDate = datetime.strptime(filterDates['filterStartDate'], '%Y-%m-%d')
            dateQuery = {
                '$or': [
                    {'filterDateList': {'$elemMatch': {'$gte': startDate}}},
                    {'filterDateList.2': {'$elemMatch': {'$gte': startDate}}},
                    {'filterDateList.3': {'$elemMatch': {'$gte': startDate}}}
                ]
            }    
        else:
            endDate =  datetime.strptime(filterDates['filterEndDate'], '%Y-%m-%d')
            dateQuery = {
                '$or': [
                    {'filterDateList': {'$elemMatch': {'$lte': endDate}}},
                    {'filterDateList.2': {'$elemMatch': {'$lte': endDate}}},
                    {'filterDateList.3': {'$elemMatch': {'$lte': endDate}}}
                ]
            }
                
    if  dateQuery != {}:
        writFilter.append(dateQuery)   
    
    print(writFilter)    

    filter = {"$and" : writFilter}
    results = writs.find(filter)
    
    if len(writFilter) == 0:
        results = writs.find().sort('WritDate',-1).limit(20)
    
    data = []
    i = 1
    for x in results:
        temp = {}
        temp['id'] = i
        i+=1
        for col in matrix:
            temp[col] = x[matrix[col]]
        data.append(temp)
    
    return JsonResponse({'success' : True, 'data' : data})
    



@require_http_methods(['POST'])
def downloadPdf(request):
    postData = json.loads(request.body)
    print(postData)
    writ_number = postData['writNumber']
    oldWrit = writs.find_one({'writNumber' : writ_number})
    file_id = ''
    for attach in attachments:
        if attach in postData:
            file_id = oldWrit[attach]
            
    file_object = gridFSWrit.get(ObjectId(file_id))
    # Set response headers to force file download
    response = HttpResponse(file_object, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{file_object.filename}"'
    return response


@require_http_methods(['POST'])
def addCounters(request):
    try:    
        counterData = request.POST
        writNumber = counterData['writNumber']
        filter = {"writNumber" : writNumber}
        oldWrit = writs.find_one(filter=filter)
        
        if counterData['flag']=='-1':
            if 'counterList' in oldWrit:    
                for counter in oldWrit['counterList']:
                    if 'counterFileAttachment' in counter and counter['counterFileAttachment'] != '':
                        gridFSWrit.delete(oldWrit['counterFileAttachment'])
            oldWrit['writMaxValue'][5-2] = 0
            oldWrit['filterDateList'][2] = []
            oldWrit['counterList'] = []
        
        elif counterData['flag'] == '1':
            if 'counterList' in oldWrit:
                for counter in oldWrit['counterList']:
                    if 'counterFileAttachment' in counter and counter['counterFileAttachment'] != '':
                        gridFSWrit.delete(oldWrit['counterFileAttachment'])
            
            currentCounters = []
            temp = {}
            for key in counterData:
                if key == 'writNumber' or key == 'flag':
                    continue
                temp[key] = counterData[key]
            
            if 'counterFileAttachment' in request.FILES and request.FILES.get('counterFileAttachment') != '':
                file = request.FILES.get('counterFileAttachment')
                file_id = gridFSWrit.put(file.read(), filename=file.name)
                temp['counterFileAttachment'] = str(file_id)
        
            currentCounters.append(temp)
            oldWrit['filterDateList'][2] = [datetime.strptime(counterData['counterDate'], '%Y-%m-%d') ]
            oldWrit['counterList'] = currentCounters
            oldWrit['writMaxValue'][5-2] = 1
            
        else:
            temp = {}
            for key in counterData:
                if key == 'writNumber' or key == 'flag':
                    continue
                temp[key] = counterData[key]
            
            if 'counterFileAttachment' in request.FILES and request.FILES.get('counterFileAttachment') != '':
                file = request.FILES.get('counterFileAttachment')
                file_id = gridFSWrit.put(file.read(), filename=file.name)
                temp['counterFileAttachment'] = str(file_id)
            
            oldWrit['filterDateList'][2].append(datetime.strptime(counterData['counterDate'], '%Y-%m-%d'))
            oldWrit['counterList'].append(temp)
            oldWrit['writMaxValue'][5-2] = 1

        writs.replace_one(filter, oldWrit)
        # print(oldWrit)
        return JsonResponse({'success' : True})
    except Exception as err:
        return JsonResponse({'success' : False, 'error' : err})
  
    
@require_http_methods(['POST'])
def addCourtOrder(request):
    try:    
        counterData = request.POST
        writNumber = counterData['writNumber']
        filter = {"writNumber" : writNumber}
        oldWrit = writs.find_one(filter=filter)
        
        if counterData['flag']=='-1':
            if 'courtOrderList' in oldWrit:    
                for counter in oldWrit['courtOrderList']:
                    if 'courtOrderFileAttachment' in counter and counter['courtOrderFileAttachment'] != '':
                        gridFSWrit.delete(oldWrit['courtOrderFileAttachment'])
            oldWrit['writMaxValue'][5-3] = 0
            oldWrit['filterDateList'][3] = []
            oldWrit['courtOrderList'] = []
        
        elif counterData['flag'] == '1':
            if 'courtOrderList' in oldWrit:
                for counter in oldWrit['courtOrderList']:
                    if 'courtOrderFileAttachment' in counter and counter['courtOrderFileAttachment'] != '':
                        gridFSWrit.delete(oldWrit['courtOrderFileAttachment'])
            
            currentCounters = []
            temp = {}
            for key in counterData:
                if key == 'writNumber' or key == 'flag':
                    continue
                temp[key] = counterData[key]
            
            if 'courtOrderFileAttachment' in request.FILES and request.FILES.get('courtOrderFileAttachment') != '':
                file = request.FILES.get('courtOrderFileAttachment')
                file_id = gridFSWrit.put(file.read(), filename=file.name)
                temp['courtOrderFileAttachment'] = str(file_id)
        
            currentCounters.append(temp)
            oldWrit['filterDateList'][3] = [datetime.strptime(counterData['courtOrderDate'], '%Y-%m-%d') ]
            oldWrit['courtOrderList'] = currentCounters
            oldWrit['writMaxValue'][5-3] = 1
            
        else:
            temp = {}
            for key in counterData:
                if key == 'writNumber' or key == 'flag':
                    continue
                temp[key] = counterData[key]
            
            if 'courtOrderFileAttachment' in request.FILES and request.FILES.get('courtOrderFileAttachment') != '':
                file = request.FILES.get('courtOrderFileAttachment')
                file_id = gridFSWrit.put(file.read(), filename=file.name)
                temp['courtOrderFileAttachment'] = str(file_id)
            
            oldWrit['filterDateList'][3].append(datetime.strptime(counterData['courtOrderDate'], '%Y-%m-%d'))
            oldWrit['courtOrderList'].append(temp)
            oldWrit['writMaxValue'][5-3] = 1

        writs.replace_one(filter, oldWrit)
        # print(oldWrit)
        return JsonResponse({'success' : True})
    except Exception as err:
        return JsonResponse({'success' : False, 'error' : err})
  
    

@require_http_methods(['POST'])
def getCounters(request):
    try:
        writNumber = json.loads(request.body).get('writNumber',None)
        if writNumber == '':
            return JsonResponse({'success' : True, 'data' : []})
        filter = {"writNumber" : writNumber}
        oldWrit = writs.find_one(filter=filter)
        if 'counterList' not in oldWrit:
            return JsonResponse({'success' : True, 'data' : []})
        postData = oldWrit['counterList']
        return JsonResponse({'success' : True, 'data' : postData})
    except Exception as err:
        return JsonResponse({'success':False,'error':'problem in getting third.js from backend'})

        
        
    # data = json.loads(request.body)
    # print(data)
    
    
@require_http_methods(['POST'])
def getCourtOrders(request):
    try:
        writNumber = json.loads(request.body).get('writNumber',None)
        if writNumber == '':
            return JsonResponse({'success' : True, 'date' : []})
        filter = {"writNumber" : writNumber}
        oldWrit = writs.find_one(filter=filter)
        if 'courtOrderList' not in oldWrit:
            return JsonResponse({'success' : True, 'data' : []})
        postData = oldWrit['courtOrderList']
        return JsonResponse({'success' : True, 'data' : postData})
    except Exception as err:
        return JsonResponse({'success':False,'error':'problem in getting third.js from backend'})


@require_http_methods(['POST'])
def hemang(request):
    try:
        data = request.POST
        print(data['writClose'] == 'true')
        JsonResponse({'success': True, 'error': 'request data empty'})
    except Exception as err:
        return JsonResponse({'success':False, 'error':err})