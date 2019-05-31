from django.db import models
from classInfo.models import Teacher
from textInteraction.models import TextModelBasicInfo


class CooperationModels(models.Model):
    # TRAIN_STATUS_CHOICES = (
    #     (1, "已训练"),
    #     (0, "未训练")
    # )
    #
    DELETE_STATUS_CHOICES = (
        (1, "已删除"),
        (0, "未删除")
    )

    cn_name = models.CharField(max_length=20)
    en_name = models.CharField(max_length=20, primary_key=True)
    teacher_belong = models.ForeignKey(Teacher)
    algorithm = models.CharField(max_length=5)
    accuracy = models.FloatField(null=True)
    loss = models.FloatField(null=True)
    labels = models.TextField(max_length=65535)
    label_content = models.TextField(max_length=65535)
    contents = models.TextField(max_length=65535)
    # train_status = models.IntegerField(verbose_name="训练状态", choices=TRAIN_STATUS_CHOICES, default=0)
    delete_status = models.IntegerField(verbose_name="删除状态", choices=DELETE_STATUS_CHOICES, default=0)
    data_create = models.DateTimeField(auto_now_add=True)
    data_update = models.DateTimeField(auto_now=True)


class CooperationData(models.Model):
    en_name = models.ForeignKey(TextModelBasicInfo)
    student_name = models.CharField(max_length=20)
    label_content = models.TextField(max_length=65535)
    contents = models.TextField(max_length=65535)
    data_create = models.DateTimeField(auto_now_add=True)
    data_update = models.DateTimeField(auto_now=True)
