from rest_framework import permissions
from  datetime import datetime
import pytz

from contest import models as modelsCo
from rest_framework.exceptions import PermissionDenied
from player import models as modelsPl


class IsAllowedToLogin(permissions.BasePermission):
    message = "You are not allowed to log in before the contest starts."

    def has_permission(self, request, view):
        user = request.user
        try:
            login_allow = modelsPl.LoginAllow.objects.get(user=user)
            return True  # User belongs to a LoginAllow instance, so they are allowed to log in.
        except modelsPl.LoginAllow.DoesNotExist:
            return False  # User does not belong to a LoginAllow instance, so they are not allowed to log in.



class TimecheckLogin(IsAllowedToLogin):
    message = "Contest has not started yet."

    def has_permission(self, request, view):
        currentTime = datetime.now(tz=pytz.UTC)
        try:
            try:
                contestQuery = modelsCo.Contest.objects.get(contestId=request.data["contestId"])
            except:
                self.message = "Contest Does not exists."
                return False
            try :
                user = modelsPl.User.objects.get(username=request.data["username"])
                login_allow = modelsPl.LoginAllow.objects.filter(user=user).exists()
                print(login_allow)
                if login_allow :
                    return True
            except:
                pass
            
            if  contestQuery.endTime <= currentTime :
                self.message = 'Contest Has Ended.'
                return False
           
            if not contestQuery.isStarted:
                self.message = "Contest has not started yet.(p)"
                return False
            
            return contestQuery.startTime <= currentTime
        except:
            return True


class TimecheckGlobal(permissions.BasePermission):
    message = "Contest has not started yet.(p)"

    def has_permission(self, request, view):
        currentTime = datetime.now(tz=pytz.UTC)
        try:
            try:
                contestQuery = modelsCo.Contest.objects.get(contestId=view.kwargs["contestId"])
            except:
                self.message = "Contest Does not Exists.(p)"
                return False
            if not contestQuery.isStarted:
                self.message = "Contest has not started yet.(p)"
                return False
            if  contestQuery.endTime <= currentTime :
                self.message = 'Contest Has Ended.(p)'
                return False
            return contestQuery.startTime <= currentTime
        except:
            return True


