from .models import *
from contest import models as modelsCo

def getContainer():
    container = modelsCo.Container.objects.filter(status=False).exists()
    if container:
        containerId = modelsCo.Container.objects.filter(status=False).first()
        containerId.status = True
        containerId.count+=1
        containerId.save()
        return containerId.containerId
    return False

def deallocate(containerid):
    container = modelsCo.Container.objects.get(containerId=containerid)
    container.status = False
    container.save()