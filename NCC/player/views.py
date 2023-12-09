from .models import *
from .serializers import *
from django.views import View
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

from contest.models import Contest


from core.permissions import TimecheckLogin


#############################
#                           #
#        Login Api          #
#                           #
#############################

class LoginApi(generics.CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes=[TimecheckLogin]
    
    
    def post(self, request, format=None):


        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')
        contestId = serializer.validated_data.get('contestId')

        user = authenticate(username=username, password=password)
        print("user ...",user)
        if user is not None:
            print("Authenticated but not in team")
            try:
                team = Team.objects.get(Q(user1 = user) | Q(user2 = user),contest=contestId)
                print(team)
                if (team.isLogin):
                    return Response({'msg':'You are Already Logged in'}, status=status.HTTP_400_BAD_REQUEST)
                
                # if user is not None:
                token = RefreshToken.for_user(user=user)
                
                # team.isLogin = True
                team.save()
                data = {
                    'token': str(token.access_token),
                    'isJunior' : team.isJunior,
                    'contestId' : contestId
                }
                return Response(data, status=status.HTTP_200_OK)
            except:
                return Response({'msg':'Try to contact organiser'}, status=status.HTTP_404_NOT_FOUND)
        else:
            # If user not present in local db
            # Try on main website API
            # request 
            URL="https://api.ctd.credenz.in/api/verify/NCC/"

            responce = requests.get(url = URL+username)
            responceData = responce.json()
            if (responceData.get("success")):
                if (responceData.get("team_password") == password):
                    user = User.objects.create(username = username,password = password)
                    team = Team.objects.create(user1 = user)

                    token = RefreshToken.for_user(user=user)
                
                    team.isLogin = True
                    team.save()
                    data = {
                        'token': str(token.access_token),
                        'isJunior' : team.isJunior
                    }
                    return Response(data, status=status.HTTP_200_OK)
                else:
                    return Response({'msg':'Incorrect Password'}, status=status.HTTP_401_UNAUTHORIZED)
                        
        return Response({'msg':'User not Found'},status=status.HTTP_404_NOT_FOUND)
    



# Write api to avoid mail service fail
'''
User will give its credential of main web not contest cred 
on main web just check is this user registered to event if yes give data

*Note - Make only if problem like CTD23 occures 
'''