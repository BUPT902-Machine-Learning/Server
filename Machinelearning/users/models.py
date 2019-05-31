from django.db import models


class Users(models.Model):
    username = models.CharField(max_length=20, primary_key=True)
    user_permission = models.IntegerField(default=0, null=True)
    password = models.CharField(max_length=20, null=True)
    token = models.CharField(max_length=256)


class Student(models.Model):
    student_name = models.CharField(max_length=20, primary_key=True)
    class_no = models.CharField(max_length=20)
