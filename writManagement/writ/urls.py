from django.urls import path
from . import  views 
urlpatterns = [
    path('addNewWrit',views.addNewWrit),
    path('getLatestWrit',views.getLatestWrit),
    path('getWrit', views.getWrit),
    path('filterWrit', views.filterWrit),
    path('downloadPdf', views.downloadPdf),
    path('addCounters', views.addCounters),   
    path('getCounters', views.getCounters),
    path('addCourtOrder', views.addCourtOrder),
    path('getCourtOrders', views.getCourtOrders),
    path('deleteWrit', views.deleteWrit),
    # path('hemang', views.hemang),
]