from django.urls import path
from . import  views 
urlpatterns = [
    path('get_all_departments',views.get_all_departments),
    path('get_meetings',views.get_meetings),
]