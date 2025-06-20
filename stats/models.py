from django.conf import settings
from django.db import models


class Semester(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    start_date = models.DateField()
    end_date = models.DateField()
    is_running = models.BooleanField(default=False)
    auto_add_to_group = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Course(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    course_code = models.CharField(max_length=10)
    credit = models.FloatField()
    section = models.CharField(max_length=5)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    is_retake = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


class Assessment(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    assessment_type = models.ForeignKey('Assessment_Type', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    total_marks = models.FloatField()
    expected_marks = models.FloatField()
    obtained_marks = models.FloatField()
    date = models.DateField(auto_now_add=True)  # not using now, but maybe in future

    def __unicode__(self):
        return self.name


class Assessment_Type(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    mark_percentage = models.FloatField()
    best_of = models.IntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.name
