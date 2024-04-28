import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.urls import resolve
import json
User = get_user_model()


# View for login, uses jwt token for security checks
@require_http_methods(["POST", "GET"])
def get_jwt_token(request):
    if request.method == 'GET':
        return JsonResponse({'error': 'GET Method Not Allowed'})

    try:
        user_data = json.loads(request.body)
        username = user_data['username']
        password = user_data['password']
        try :
            userName = User.objects.get(username=username)
            try : 
                user = User.objects.get(username=username, password=password)
                expiry_time = datetime.utcnow() + timedelta(days=1)
                # Create the payload with user id and expiration time
                payload = {
                    'user_id': user.pk,
                    'exp': expiry_time
                }

                # Encode the payload into a JWT token
                token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

                # Return the token as a JSON response
                return JsonResponse({'token': token, 'success': True})
            except:
                return JsonResponse({'error': 'Incorrect password', 'success': False}, status=401)
                  
        except:
            return JsonResponse({'error': 'Username not found', 'success': False}, status=404)
            
    except Exception as err:
        print(err)
        return JsonResponse({'error': 'Some Error Has Occured!', 'success': False})


# view for signup. It saves data in User django object that is connected to postgresql through settings.py
@require_http_methods(["POST"])
def signup(request):
    # Return the token as a JSON response
    try:
        user_data = json.loads(request.body)
        user_data.pop('mobile')
        user_data.pop('district')
        user_data.pop('dob')
        user_data.pop('batch')
        new_user = User.objects.create(**user_data)
        new_user.save()
        return JsonResponse({'success': True, 'message': 'user created successfully'})
    except Exception as err:
        print(err)
        return JsonResponse({'error': "Some Error Has Occured in creating auth.user!", 'success': False})
    

@require_http_methods(["GET"])
def getAllUsers(request):
    x =  User.objects.all().values()
    data = []
    for person in x:
        data.append({
            'id' : person['id'],
            'first_name' : person['first_name'],
            'last_name' : person['last_name']
        })
    return JsonResponse({'success': True, 'data': data })