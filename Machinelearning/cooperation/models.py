from django.db import models
from classInfo.models import Teacher
from textInteraction.models import TextModelBasicInfo

from users.models import Users
from django.contrib.auth.models import User


def content_save_path(instance, filename):
    path = str(instance.model_name.en_name) + "/" + str(instance.label) + "/" + filename
    print(path)
    return path


class TextCooperationModels(models.Model):
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


class NumbersCooperationModels(models.Model):
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


class TextCooperationData(models.Model):
    en_name = models.ForeignKey(TextModelBasicInfo)
    student_name = models.CharField(max_length=20)
    label_content = models.TextField(max_length=65535)
    contents = models.TextField(max_length=65535)
    data_create = models.DateTimeField(auto_now_add=True)
    data_update = models.DateTimeField(auto_now=True)


class NumbersCooperationData(models.Model):
    en_name = models.ForeignKey(TextModelBasicInfo)
    student_name = models.CharField(max_length=20)
    label_content = models.TextField(max_length=65535)
    contents = models.TextField(max_length=65535)
    data_create = models.DateTimeField(auto_now_add=True)
    data_update = models.DateTimeField(auto_now=True)


class CooperationImageModels(models.Model):
    DELETE_STATUS_CHOICES = (
        (1, "已删除"),
        (0, "未删除")
    )

    MODEL_TYPE_CHOICES = (
        (1, "普通模型"),
        (0, "合作模型")
    )

    TRAIN_STATUS_CHOICES = (
        (3, "已训练"),
        (2, "训练中"),
        (1, "已发布"),
        (0, "未发布"),
    )

    cn_name = models.CharField(max_length=20, null=True)
    en_name = models.CharField(max_length=20, primary_key=True)
    user_belong = models.ForeignKey(Users)
    labels = models.TextField(max_length=65535, null=True)
    algorithm = models.CharField(max_length=10, default="CNN-SVM")
    accuracy = models.FloatField(null=True)
    delete_status = models.IntegerField(verbose_name="删除状态", choices=DELETE_STATUS_CHOICES, default=0)
    train_status = models.IntegerField(verbose_name="训练状态", choices=TRAIN_STATUS_CHOICES, default=0)
    model_type = models.IntegerField(verbose_name="模型类型", choices=MODEL_TYPE_CHOICES, default=1)
    data_create = models.DateTimeField(auto_now_add=True)
    data_update = models.DateTimeField(auto_now=True)


class CooperationImageTrainData(models.Model):
    DELETE_STATUS_CHOICES = (
        (1, "已删除"),
        (0, "未删除")
    )
    user_belong = models.ForeignKey(Users)
    model_name = models.ForeignKey(CooperationImageModels)
    image_name = models.TextField(max_length=65535)
    content = models.ImageField(null=True, upload_to=content_save_path)
    label = models.TextField(max_length=65535)
    delete_status = models.IntegerField(verbose_name="删除状态", choices=DELETE_STATUS_CHOICES, default=0)
    data_create = models.DateTimeField(auto_now_add=True)
    data_update = models.DateTimeField(auto_now=True)


class CooperationImageLabelMap(models.Model):
    model_name = models.ForeignKey(CooperationImageModels)
    real_labels = models.TextField(max_length=65535)
    train_labels = models.TextField(max_length=65535)