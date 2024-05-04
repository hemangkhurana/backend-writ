from django.urls import path
from . import  views 
urlpatterns = [
    path('get_meetings',views.get_meetings),
    path('add_department', views.add_department),
    path('create_new_meeting', views.create_new_meeting),
    path('get_departments', views.get_departments),
    path('delete_department', views.delete_department),
    path('update_department', views.update_department),
    path('delete_meeting', views.delete_meeting),
    path('update_meeting', views.update_meeting),
    path('searchInMeeting', views.searchInMeeting)
]