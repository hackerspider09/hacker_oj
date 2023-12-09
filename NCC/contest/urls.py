from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'gettime', GetTime,basename='gettime_all')
router.register(r'gettime/(?P<contestId>[-\w]+)', GetTime,basename='gettime')


urlpatterns = [
    path('', include(router.urls)),
    
]
