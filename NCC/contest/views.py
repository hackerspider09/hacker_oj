from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.generics import mixins
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import status

#############################
#                           #
#   Get Contest Time Api    #
#                           #
#############################

class GetTime(viewsets.GenericViewSet,mixins.ListModelMixin):
    queryset = Contest.objects.all()
    serializer_class = GetTimeSerializer

    def list(self, request, *args, **kwargs):
        # Access the contestId from the URL kwargs
        contest_id = self.kwargs.get('contestId')
        print(contest_id)
        if not contest_id:
            return super().list(request, *args, **kwargs)
        try:
            contestQuery = Contest.objects.get(contestId = contest_id)
            serializer = self.serializer_class(contestQuery)
            return Response(serializer.data,status.HTTP_200_OK)
            # return super().list(request, *args, **kwargs)
        except:
            return Response({"msg":"Contest Does not Exists."},status=status.HTTP_404_NOT_FOUND)
