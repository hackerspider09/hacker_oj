from django.contrib import admin
from import_export.admin import ExportActionMixin
from .models import *



class ContestAdmin (admin.ModelAdmin):
    list_display = ("contestId","name","startTime","endTime")
admin.site.register(Contest,ContestAdmin)




class ContainerAdmin(admin.ModelAdmin):
    list_display= ("id","containerId","count","status","containerUpTime")
admin.site.register(Container,ContainerAdmin)





# class ResultAdmin(admin.ModelAdmin):
#     list_display= ('teamId','score','questions_attempted','questions_solved')
# admin.site.register(Result,ResultAdmin)


