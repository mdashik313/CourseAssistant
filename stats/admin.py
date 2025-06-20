from django.contrib import admin

from .models import Semester, Course, Assessment, Assessment_Type

# Register your models here.
admin.site.register(Semester)
admin.site.register(Course)
admin.site.register(Assessment)
admin.site.register(Assessment_Type)
