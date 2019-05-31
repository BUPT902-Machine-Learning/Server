# models.py
from django.db import models
from users.models import Users


class NumbersModelBasicInfo(models.Model):
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

    cn_name = models.CharField(max_length=20)
    en_name = models.CharField(max_length=20, primary_key=True)
    user_belong = models.ForeignKey(Users)
    labels = models.TextField(max_length=65535, null=True)
    label_content = models.TextField(max_length=65535, null=True)
    contents = models.TextField(max_length=65535, null=True)
    algorithm = models.CharField(max_length=5, null=True)
    accuracy = models.FloatField(null=True)
    loss = models.FloatField(null=True)
    delete_status = models.IntegerField(verbose_name="删除状态", choices=DELETE_STATUS_CHOICES, default=0)
    public_status = models.IntegerField(verbose_name="公开状态", choices=PUBLIC_STATUS_CHOICES, default=0)
    model_type = models.IntegerField(verbose_name="模型类型", choices=MODEL_TYPE_CHOICES, default=1)
    data_create = models.DateTimeField(auto_now_add=True)
    data_update = models.DateTimeField(auto_now=True)


class ValueSetData(models.Model):
    NUMBERS_TYPES_CHOICES = (
        (1, "数字"),
        (0, "多选")
    )

    model_name = models.ForeignKey(NumbersModelBasicInfo)
    value = models.TextField(max_length=65535)
    type = models.TextField(verbose_name="数值类型", choices=NUMBERS_TYPES_CHOICES, default=1)
    multiSelect = models.TextField(max_length=65535, null=True)


class NumbersTrainData(models.Model):
    model_name = models.ForeignKey(NumbersModelBasicInfo)
    contents = models.TextField(max_length=65535)
    labels = models.TextField(max_length=65535)
    data_create = models.DateTimeField(auto_now_add=True)
    data_update = models.DateTimeField(auto_now=True)


class NumbersLabelMap(models.Model):
    model_name = models.ForeignKey(NumbersModelBasicInfo)
    real_labels = models.TextField(max_length=65535)
    train_labels = models.TextField(max_length=65535)


class NumbersKNNParams(models.Model):
    model_name = models.ForeignKey(NumbersModelBasicInfo)
    k = models.CharField(max_length=3)


class NumbersCNNParams(models.Model):
    model_name = models.ForeignKey(NumbersModelBasicInfo)
    embedding_dim = models.CharField(max_length=5)
    num_filters = models.CharField(max_length=5)
    kernel_size = models.CharField(max_length=5)
    fully_connected_dim = models.CharField(max_length=5)
    dropout_keep_prob = models.CharField(max_length=5)
    batch_size = models.CharField(max_length=5)
    num_epochs = models.CharField(max_length=5)


class NumbersRNNParams(models.Model):
    model_name = models.ForeignKey(NumbersModelBasicInfo)
    embedding_dim = models.CharField(max_length=5)
    num_layers = models.CharField(max_length=5)
    rnn_type = models.CharField(max_length=5)
    hidden_dim = models.CharField(max_length=5)
    dropout_keep_prob = models.CharField(max_length=5)
    batch_size = models.CharField(max_length=5)
    num_epochs = models.CharField(max_length=5)


class NumbersProcessData(models.Model):
    model_name = models.ForeignKey(NumbersModelBasicInfo)
    contents = models.TextField(max_length=65535)
    labels = models.TextField(max_length=65535)
    data_count = models.IntegerField(default=0)
    seq_length = models.IntegerField(default=0)
    classes_count = models.IntegerField(default=0)
    algorithm = models.CharField(max_length=10)
    data_create = models.DateTimeField(auto_now_add=True)
