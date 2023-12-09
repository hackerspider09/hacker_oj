from rest_framework import serializers
from .models import *
from django.db.models import Q
from django.contrib.auth import authenticate
from rest_framework import serializers
from contest import models

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    contestId = serializers.CharField(required=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        contestId = attrs.get('contestId')

        if not (models.Contest.objects.filter(contestId=contestId).exists()):
            raise serializers.ValidationError({"contestId":'Contest does not exists.'})

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                # raise serializers.ValidationError('Invalid username or password.')
                attrs['user'] = None

            attrs['user'] = user
        else:
            raise serializers.ValidationError('Must include "username" and "password".')

        return attrs
