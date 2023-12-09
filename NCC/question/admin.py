from django.contrib import admin
from .models import *

class QuestionAdmin (admin.ModelAdmin):
    list_display = ("questionId","questionNumber","maxPoints","points","title","category",'contest')
admin.site.register(Question,QuestionAdmin)


class TestcaseAdmin (admin.ModelAdmin):
    list_display = ("question","testcaseNumber")
admin.site.register(Testcase,TestcaseAdmin)
