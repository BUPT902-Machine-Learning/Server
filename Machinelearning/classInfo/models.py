from django.db import models


class Teacher(models.Model):
    class_no = models.CharField(max_length=20, primary_key=True)
    teacher_name = models.CharField(max_length=20)


# class Class(models.Model):
#     STATUS_CHOICES = (
#         (1, "已开课"),
#         (0, "未开课")
#     )
#
#     class_no = models.CharField(max_length=20, primary_key=True)
#     teacher = models.ForeignKey(Teacher)
#     status = models.IntegerField(verbose_name="状态", choices=STATUS_CHOICES, default=1)
