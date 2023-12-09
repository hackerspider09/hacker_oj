from .models import *
from .serializers import *
from django.views import View
from django.shortcuts import redirect,HttpResponse
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from django.db.models import Q 
from rest_framework.generics import mixins

from django.contrib.auth import authenticate
from datetime import datetime 

# JWT
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated,IsAdminUser

from rest_framework.throttling import UserRateThrottle, ScopedRateThrottle
from rest_framework.renderers import JSONRenderer

import requests

from contest.models import Contest
from .utils import *
from .judgeUtils import *
from django.utils import timezone

from core.permissions import TimecheckGlobal
from question import models as modelsQu




#############################
#                           #
#    Submissions API        #
#                           #
#############################

class GetSubmissions(viewsets.GenericViewSet,mixins.ListModelMixin):
    '''This view get parameters from url'''
    
    queryset = Submission.objects.all()
    serializer_class = GetSubmissionSerializer
    lookup_field="question"
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,TimecheckGlobal] 

    def get_queryset(self):
        user = self.request.user
        contest_id = self.kwargs['contestId']
        print(contest_id)

        team = Team.objects.get(Q(user1 = user)| Q(user2 = user),contest=contest_id)
        queryset = super().get_queryset()
        queryset = queryset.filter(team = team).order_by("-id")
        

        question = self.request.query_params.get("question")
        if question:    
            # print("Users Question => ",question)
            queryset = queryset.filter(question=question)
        
            
        return queryset
    
    # http://127.0.0.1:8000/api/submissions/?question=fa152
        


#############################
#                           #
#         Submit API        #
#                           #
#############################

class Submit(viewsets.GenericViewSet,mixins.CreateModelMixin):

    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    renderer_classes = [JSONRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,TimecheckGlobal]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'submit'

    def create(self, request, *args, **kwargs):
        
        data = request.data
        contest_id = self.kwargs['contestId']
        
        # print("=> Requested Data ",data)
        serializer = SubmissionSerializer(data=data)
        if serializer.is_valid():

            container = getContainer()
            if not container:
                return   Response({'msg':"Server is Busy"},status=status.HTTP_403_FORBIDDEN)
            

            user = self.request.user
            userId = user.id
            team = Team.objects.get(Q(user1 = user) | Q(user2 = user),contest=contest_id)
            # team = serializer.validated_data['team']

            code = serializer.validated_data['code']
            language = serializer.validated_data['language']
            question = serializer.validated_data['question']

            input = serializer.validated_data.pop('input', "")
            # print("=> Serialized Data ",input)
            isSubmitted = True
            try:
                print("*******Valid  and saved*******")
                
                codeStatus=  runCode(question,code,language,isSubmitted,container,input)
                deallocate(container)
                # return_code_testcase1 = codeStatus["testcase1"]["returnCode"]    #One method to get rc from runCode 
                # print("Return code of testcase1:", return_code_testcase1)
                
                returnCodeList = []
                for testcase, values in codeStatus.items():
                    returnCodeList.append(values["returnCode"])
                
                # print(returnCodeList)
                if (returnCodeList.count(0) == len(returnCodeList)):
                    #It will work when user get all AC submission
                    
                    serializer.validated_data['status'] = ErrorCodes[0]

                    score = self.getMaxScore(question,team,contest_id)
                    # print("************ score ",score )
                    serializer.validated_data['points'] = score
                    serializer.validated_data['isCorrect'] = True

                    try:
                        lastSubmissionNumber = Submission.objects.filter(question=question,team=team).last().attemptedNumber
                        serializer.validated_data['attemptedNumber'] = lastSubmissionNumber+1
                    except:
                        serializer.validated_data['attemptedNumber'] = 1

                    serializer.validated_data['team'] = team
                    serializer.validated_data['contest'] = contest_id
                    serializer.save()

                    #This team query to save users score and last update in score
                    teamQuery= Team.objects.get(teamId = team)

                    if score !=0:
                        '''to solve this bug
                            # if user submite wrong submission there will no change in lastUpdate
                            # but if user again submit submission there is'''
                        teamQuery.score += score
                        teamQuery.lastUpdate = timezone.now()
                        teamQuery.save()
                else:
                    #When answer is other than AC
                    serializer.validated_data['status'] = ErrorCodes[returnCodeList[-1]]
            
                    serializer.validated_data['points'] = 0
                    serializer.validated_data['isCorrect'] = False

                    try:
                        lastSubmissionNumber = Submission.objects.filter(question=question,team=team).last().attemptedNumber
                    except:
                        lastSubmissionNumber = 0
                    serializer.validated_data['attemptedNumber'] = lastSubmissionNumber+1
                    serializer.validated_data['team'] = team
                    serializer.validated_data['contest'] = contest_id
                    serializer.save()

                # print(question.questionId)    #to get question id from question 
                
                return Response(codeStatus)
            except:
                deallocate(container)
                return Response({'msg':"Server is Busy"})
        else:
            print("*******Invalid*******")
            # print(request.data)
            return Response({'msg':serializer.errors})
        

    def getMaxScore(self,question,team,contest):
        questionQuery = modelsQu.Question.objects.get(questionId=question.questionId)
        # if (questionQuery.category != team.isJunior):
        #     #if user is trying another category question
        #     return 0
        
        points = questionQuery.points
        maxPoints = questionQuery.maxPoints
        print("inside get score ",question , team)
        
        try:
            submissionQuery = Submission.objects.filter(team = team ,question = question,contest=contest,isCorrect=True).exists()
            if submissionQuery:
                print("Right submission exits")
                return 0
            else:
                if (questionQuery.points-1 >= 10):
                    questionQuery.points -=1
                    questionQuery.save()

                try:
                    submissionQuery = Submission.objects.filter(team = team ,question = question,contest=contest,isCorrect = False).exists()
                    if submissionQuery:
                        penalty = Submission.objects.filter(team = team ,question = question,contest=contest).last().attemptedNumber
                        
                        score = int(points - (penalty * 0.1 * points))
                        # print("points -> ",points,"\n maxpoints -> ",maxPoints)
                        # print("penalty -> ",penalty,"\nScore -> ",score)

                        if score > 0:
                            print("score > 0")
                            return score
                        print("score < 0")
                        #User will get 10 points if its score is negative for right submission
                        return 10
                    else:
                        return points
                except:
                    print("score = maxpoints")
                    return points
        except:
            print("None value is returing ")
            pass



#############################
#                           #
#       Run Code API        #
#                           #
#############################

class RunCode(generics.GenericAPIView):
    serializer_class = SubmissionSerializer
    renderer_classes = [JSONRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,TimecheckGlobal]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'submit'

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            container = getContainer()

            try:
                if not container:
                    return   Response({'msg':"Server is Busy"},status=status.HTTP_403_FORBIDDEN)
            
                print("*******Valid but not saved*******")
                code = serializer.validated_data['code']
                language = serializer.validated_data['language']
                question = serializer.validated_data['question']
                input = serializer.validated_data['input']
                isSubmitted = False
                
                codeStatus=  runCode(question,code,language,isSubmitted,container,input)
                # codeStatus = codeStatus.get()
                deallocate(container)
                serializer.validated_data['input'] = input
                codeStatus.update(serializer.data)
                responce = codeStatus
                # print("responce => ",responce)
                return Response(codeStatus)
            
            except:
                deallocate(container)
                return Response({'msg':"Server is Busy."})
            
        return Response(serializer.validated_data, status=status.HTTP_200_OK)



def RunRcUtil(question,ip,container):

    correctCodeQuery = CorrectCode.objects.get(question__questionId = question)
    codeStatus=  runCode(correctCodeQuery.question,correctCodeQuery.correct_code,correctCodeQuery.language,False,container,ip)
    # print(codeStatus)
    return {"output":codeStatus.get('output')}


class RunRc(generics.GenericAPIView):

    queryset = Submission.objects.all()
    serializer_class = RcSubmissionSerializer
    renderer_classes = [JSONRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,TimecheckGlobal]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'rc'
        
    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            container = getContainer()

            try:
                if not container:
                    return   Response({'msg':"Server is Busy"},status=status.HTTP_403_FORBIDDEN)
            
                print("*******Rc IP OP functnality ******")
                question = serializer.validated_data['question']
                input = serializer.validated_data['input']
                codeStatus=  RunRcUtil(question,input,container)
                # print("ffff => ",codeStatus)
                serializer.validated_data['output'] = codeStatus
                codeStatus.update(serializer.data)
                # codeStatus = serializer.data
                # print("responce => ",codeStatus)
                deallocate(container)
                return Response(codeStatus)
            
            except:
                deallocate(container)
                return Response({'msg':"Server is Busy."})
            
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
