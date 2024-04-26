from django.urls import path
from . import  views 
urlpatterns = [
    path('get_all_departments',views.get_all_departments),
    path('get_meetings',views.get_meetings),
    path('add_department', views.add_department),
    path('hemang', views.hemang),
    path('get_departments', views.get_departments),
]