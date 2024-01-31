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
# Create your views here.

@require_http_methods(["POST", "GET"])
def get_jwt_token(request):
    if (request.method == 'GET'):
        return JsonResponse({'error': 'GET Method Not Allowed'})
    else:
        try:
            print("opppppppppppp")
            user_data = json.loads(request.body)
            # print(json.loads(request.body.decode()))
            username = user_data['username']
            password = user_data['password']
            # Authenticate the user
            user = User.objects.get(username=username, password=password)
            # print(user.pk)
            if user is None:
                return JsonResponse({'error': 'Invalid credentials', 'success': False}, status=401)
            # Set the expiration time for the token
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
        except Exception as err:
            print(err)
            return JsonResponse({'error': 'Some Error Has Occured!', 'success': False})



@require_http_methods(["POST"])
def signup(request):
    # Return the token as a JSON response
    # user_data
    try:
        user_data = json.loads(request.body)
        user_data.pop('mobile')
        user_data.pop('district')
        user_data.pop('dob')
        user_data.pop('batch')
        new_user = User.objects.create(**user_data)
        new_user.save()
    except Exception as err:
        print(err)
        return JsonResponse({'error': "Some Error Has Occured in creating auth.user!", 'success': False})
