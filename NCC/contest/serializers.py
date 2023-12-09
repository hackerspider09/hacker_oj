from rest_framework import serializers
from .models import *


class GetTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = "__all__"