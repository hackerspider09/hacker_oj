from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'(?P<contestId>[-\w]+)/submissions', GetSubmissions,basename='submissions')
router.register(r'(?P<contestId>[-\w]+)/submit', Submit,basename='submit')


urlpatterns = [
    path('', include(router.urls)),
    path('<str:contestId>/runcode/',RunCode.as_view(),name="Run code"),
    path('<str:contestId>/runrccode/',RunRc.as_view(),name="Run code"),
]
