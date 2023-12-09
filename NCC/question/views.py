from .models import *
from .serializers import *
from django.views import View
from rest_framework import viewsets
from rest_framework.generics import mixins
from django.shortcuts import redirect,HttpResponse
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from django.db.models import Q 

from django.contrib.auth import authenticate
from datetime import datetime 

# JWT
from rest_framework_simplejwt.tokens import RefreshToken


import requests

from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated,IsAdminUser

from player.models import Team
from rest_framework_simplejwt.authentication import JWTAuthentication


from core.permissions import TimecheckGlobal



#############################
#                           #
#     Question API          #
#                           #
#############################

class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    To get question list respective to category (Junior,Senior,Both)
    To get specific question by question ID from URL
    '''
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    lookup_field="questionId"
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,TimecheckGlobal]    
    renderer_classes = [JSONRenderer]

    

    def get_queryset(self):
        print(self.kwargs['contestId'])
        contestId = self.kwargs['contestId']
        user = self.request.user
        queryset = super().get_queryset()
        print(user)
        team = Team.objects.get(Q(user1 = user) | Q(user2 = user),contest=contestId)
        return queryset.filter(Q(category= "junior" if team.isJunior else "senior" ) | Q(category="both"),contest = contestId).order_by("questionNumber")  #return  questions filtered with two  conditions

