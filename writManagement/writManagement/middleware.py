import jwt
from django.conf import settings
from django.http import JsonResponse
from django.conf import settings
from django.urls import resolve
from django.contrib.auth import  get_user_model


def JWTAuthenticationMiddleware(get_response):
    def middleware(request):
        User=get_user_model()
        # print(request.META.get('PATH_INFO'))
        if request.META.get('PATH_INFO') in ['/user/signup','/admin/','/admin/login/', '/user/login']:
            response = get_response(request)
            return response
        else:
            # Get the JWT token from the request headers
            auth_header = request.headers.get('Authorization')
            if auth_header is None or not auth_header.startswith('Bearer '):
                return JsonResponse({'error': 'Unauthorized access'})

            token = auth_header.split(' ')[1]

            try:
                # Decode the token and get the user id
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                user_id = payload.get('user_id')

                # Set the user object on the request
                # print(user_id)
                request.user = User.objects.get(pk=user_id)
            except jwt.ExpiredSignatureError:
                return JsonResponse({'error': 'Token has expired'}, status=401)

            except (jwt.DecodeError, User.DoesNotExist):
                return JsonResponse({'error': 'Invalid token'}, status=401)

            response = get_response(request)
            return response
    return middleware