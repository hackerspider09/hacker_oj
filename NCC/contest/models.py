from django.db import models
import uuid
from datetime import datetime
import pytz

class Contest(models.Model):
    contestId = models.CharField(max_length=10, primary_key=True, editable=False)
    name = models.CharField(max_length=50)
    startTime = models.DateTimeField(blank=True)
    endTime = models.DateTimeField(blank=True)
    isStarted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.contestId:
            self.contestId = str(uuid.uuid4())[:5]
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.contestId}"






class Container(models.Model):
    containerId = models.IntegerField()
    status = models.BooleanField(default=False)
    count = models.IntegerField(default=0)
    upTime = models.DateTimeField(auto_now=True)


    @property
    def containerUpTime(self):
        '''To check Up time of container'''
        currentTime = datetime.now(tz=pytz.UTC)
        timeDifference = currentTime - self.upTime
        return timeDifference
        # return 2





# class Result(models.Model):
#     teamId = models.CharField(max_length=10, primary_key=True, editable=False)
#     isLogin = models.BooleanField(default=False)
#     score = models.IntegerField(default=0)
#     isJunior = models.BooleanField(default=True)
#     questions_attempted = models.IntegerField(default=0)
#     questions_solved = models.IntegerField(default=0)
