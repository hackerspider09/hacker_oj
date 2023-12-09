from django.contrib import admin
from django.urls import path,include
from .views import LoginApi

urlpatterns = [
    path('login/', LoginApi.as_view(),name="login"),
]



