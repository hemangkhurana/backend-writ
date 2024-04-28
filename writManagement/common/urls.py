from django.urls import path
from . import  views 
urlpatterns = [
    path('login',views.get_jwt_token),
    path('signup',views.signup),
    path('getAllUsers',views.getAllUsers),
]