
from users.models import Users
from django.db import models
from django.contrib.auth.models import User
import uuid
import os


def content_save_path(instance, filename):
    path = str(instance.model_name.en_name) + "/" + str(instance.label) + "/" + filename
    print(path)
    return path


class ImageModelBasicInfo(models.Model):
    DELETE_STATUS_CHOICES = (
        (1, "已删除"),
        (0, "未删除")
    )

    PUBLIC_STATUS_CHOICES = (
        (1, "已公开"),
        (0, "未公开")
    )

    MODEL_TYPE_CHOICES = (
        (1, "普通模型"),
        (0, "合作模型")
    )

    TRAIN_STATUS_CHOICES = (
        (2, "已训练"),
        (1, "训练中"),
        (0, "未训练")
    )

    cn_name = models.CharField(max_length=20, null=True)
    en_name = models.CharField(max_length=20, primary_key=True)
    user_belong = models.ForeignKey(Users)
    labels = models.TextField(max_length=65535, null=True)
    algorithm = models.CharField(max_length=10, default="Untrained")
    accuracy = models.FloatField(null=True)
    delete_status = models.IntegerField(verbose_name="删除状态", choices=DELETE_STATUS_CHOICES, default=0)
    public_status = models.IntegerField(verbose_name="公开状态", choices=PUBLIC_STATUS_CHOICES, default=0)
    train_status = models.IntegerField(verbose_name="训练状态", choices=TRAIN_STATUS_CHOICES, default=0)
    model_type = models.IntegerField(verbose_name="模型类型", choices=MODEL_TYPE_CHOICES, default=1)
    data_create = models.DateTimeField(auto_now_add=True)
    data_update = models.DateTimeField(auto_now=True)


class TrainData(models.Model):
    DELETE_STATUS_CHOICES = (
        (1, "已删除"),
        (0, "未删除")
    )
    image_id = models.IntegerField(primary_key=True)
    user_belong = models.ForeignKey(Users)
    model_name = models.ForeignKey(ImageModelBasicInfo)
    image_name = models.TextField(max_length=65535)
    content = models.ImageField(null=True, upload_to=content_save_path)
    label = models.TextField(max_length=65535)
    delete_status = models.IntegerField(verbose_name="删除状态", choices=DELETE_STATUS_CHOICES, default=0)
    data_create = models.DateTimeField(auto_now_add=True)
    data_update = models.DateTimeField(auto_now=True)


class LabelMap(models.Model):
    model_name = models.ForeignKey(ImageModelBasicInfo)
    real_labels = models.TextField(max_length=65535)
    train_labels = models.TextField(max_length=65535)