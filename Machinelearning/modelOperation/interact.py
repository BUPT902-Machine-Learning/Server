import time
import datetime

from imageInteraction.models import ImageModelBasicInfo
from numbersInteraction.models import NumbersModelBasicInfo
from textInteraction.models import TextModelBasicInfo, TextTrainData, TextCNNParams, TextLabelMap, TextRNNParams, TextKNNParams
from users.models import Student
from classInfo.models import Teacher


def utc2local(utc_st):
    now_stamp = time.time()
    local_time = datetime.datetime.fromtimestamp(now_stamp)
    utc_time = datetime.datetime.utcfromtimestamp(now_stamp)
    offset = local_time - utc_time
    local_st = utc_st + offset
    return local_st


def get_models(username):
    models = []
    db_models = TextModelBasicInfo.objects.filter(user_belong=username, delete_status=0)
    for item in db_models:
        model = {}
        data_create = utc2local(item.data_create)
        data_update = utc2local(item.data_update)
        model["cn_name"] = item.cn_name
        model["algorithm"] = item.algorithm
        model["data_create"] = data_create.strftime("%Y-%m-%d %H:%M:%S")
        model["data_update"] = data_update.strftime("%Y-%m-%d %H:%M:%S")
        models.append(model)

    return models


def delete_models(username, model_name, data_type):
    try:
        if data_type == "文本":
            TextModelBasicInfo.objects.filter(user_belong=username, cn_name=model_name).update(delete_status=1)
        elif data_type == "数字":
            NumbersModelBasicInfo.objects.filter(user_belong=username, cn_name=model_name).update(delete_status=1)
        else:
            ImageModelBasicInfo.objects.filter(user_belong=username, cn_name=model_name).update(delete_status=1)

    except Exception as e:
        return "delete_error"

    return "delete_confirm"


def edit_models(username, model_name):
    response = TextModelBasicInfo.objects.get(user_belong=username, cn_name=model_name)
    en_name = response.en_name
    algorithm = response.algorithm

    response_train_data = TextTrainData.objects.filter(model_name=en_name)
    response_real_labels = TextLabelMap.objects.get(model_name=en_name)
    params = {}
    if algorithm == "CNN":
        response_params = TextCNNParams.objects.get(model_name=en_name)
        params["embedding_dim"] = response_params.embedding_dim
        params["num_filters"] = response_params.num_filters
        params["kernel_size"] = response_params.kernel_size
        params["fully_connected_dim"] = response_params.fully_connected_dim
        params["dropout_keep_prob"] = response_params.dropout_keep_prob
        params["batch_size"] = response_params.batch_size
        params["num_epochs"] = response_params.num_epochs

    elif algorithm == "RNN":
        response_params = TextRNNParams.objects.get(model_name=en_name)
        params["embedding_dim"] = response_params.embedding_dim
        params["num_layers"] = response_params.num_layers
        params["rnn_type"] = response_params.rnn_type
        params["hidden_dim"] = response_params.hidden_dim
        params["dropout_keep_prob"] = response_params.dropout_keep_prob
        params["batch_size"] = response_params.batch_size
        params["num_epochs"] = response_params.num_epochs

    elif algorithm == "KNN":
        response_params = TextKNNParams.objects.get(model_name=en_name)
        params["k"] = response_params.k

    length = len(response_train_data)
    contents = response_train_data[length - 1].contents.split(';')
    labels = response_train_data[length - 1].labels.split(';')
    real_labels = response_real_labels.real_labels.split(';')
    train_data = []
    for i in range(len(real_labels)):
        data = {}
        data["label"] = real_labels[i]
        data["contents"] = []
        for label, content in zip(labels, contents):
            if label == str(i):
                data["contents"].append(content)

        train_data.append(data)

    return train_data, params, algorithm, response.public_status


def teach_get_models(username, class_no):
    my_models = []
    stu_models = []

    db_models = TextModelBasicInfo.objects.filter(user_belong=username, delete_status=0, model_type=1)
    for item in db_models:
        model = {}
        data_create = utc2local(item.data_create)
        data_update = utc2local(item.data_update)
        model["cn_name"] = item.cn_name
        model["data_type"] = "文本"
        model["algorithm"] = item.algorithm
        model["data_create"] = data_create.strftime("%Y-%m-%d %H:%M:%S")
        model["data_update"] = data_update.strftime("%Y-%m-%d %H:%M:%S")
        my_models.append(model)

    db_models = NumbersModelBasicInfo.objects.filter(user_belong=username, delete_status=0, model_type=1)
    for item in db_models:
        model = {}
        data_create = utc2local(item.data_create)
        data_update = utc2local(item.data_update)
        model["cn_name"] = item.cn_name
        model["data_type"] = "数字"
        model["algorithm"] = item.algorithm
        model["data_create"] = data_create.strftime("%Y-%m-%d %H:%M:%S")
        model["data_update"] = data_update.strftime("%Y-%m-%d %H:%M:%S")
        my_models.append(model)

    db_models = ImageModelBasicInfo.objects.filter(user_belong=username, delete_status=0, model_type=1)
    for item in db_models:
        model = {}
        data_create = utc2local(item.data_create)
        data_update = utc2local(item.data_update)
        model["cn_name"] = item.cn_name
        model["data_type"] = "图片"
        model["algorithm"] = item.algorithm
        model["data_create"] = data_create.strftime("%Y-%m-%d %H:%M:%S")
        model["data_update"] = data_update.strftime("%Y-%m-%d %H:%M:%S")
        my_models.append(model)

    db_student = Student.objects.filter(class_no=class_no)

    for item in db_student:
        db_models = TextModelBasicInfo.objects.filter(user_belong=item.student_name, delete_status=0, public_status=1)
        stu_model = []
        for item2 in db_models:
            model = {}
            data_create = utc2local(item2.data_create)
            data_update = utc2local(item2.data_update)
            model["user_name"] = item.student_name
            model["cn_name"] = item2.cn_name
            model["data_type"] = "文本"
            model["algorithm"] = item2.algorithm
            model["data_create"] = data_create.strftime("%Y-%m-%d %H:%M:%S")
            model["data_update"] = data_update.strftime("%Y-%m-%d %H:%M:%S")
            stu_model.append(model)

        db_models = NumbersModelBasicInfo.objects.filter(user_belong=item.student_name, delete_status=0, public_status=1)
        stu_model = []
        for item2 in db_models:
            model = {}
            data_create = utc2local(item2.data_create)
            data_update = utc2local(item2.data_update)
            model["user_name"] = item.student_name
            model["cn_name"] = item2.cn_name
            model["data_type"] = "数字"
            model["algorithm"] = item2.algorithm
            model["data_create"] = data_create.strftime("%Y-%m-%d %H:%M:%S")
            model["data_update"] = data_update.strftime("%Y-%m-%d %H:%M:%S")
            stu_model.append(model)

        db_models = ImageModelBasicInfo.objects.filter(user_belong=item.student_name, delete_status=0, public_status=1)
        stu_model = []
        for item2 in db_models:
            model = {}
            data_create = utc2local(item2.data_create)
            data_update = utc2local(item2.data_update)
            model["user_name"] = item.student_name
            model["cn_name"] = item2.cn_name
            model["data_type"] = "图片"
            model["algorithm"] = item2.algorithm
            model["data_create"] = data_create.strftime("%Y-%m-%d %H:%M:%S")
            model["data_update"] = data_update.strftime("%Y-%m-%d %H:%M:%S")
            stu_model.append(model)

        stu_models.append(stu_model)

    return my_models, stu_models


def stu_get_models(username, class_no):
    my_models = []
    teach_models = []

    db_models = TextModelBasicInfo.objects.filter(user_belong=username, delete_status=0)
    for item in db_models:
        model = {}
        data_create = utc2local(item.data_create)
        data_update = utc2local(item.data_update)
        model["cn_name"] = item.cn_name
        model["data_type"] = "文本"
        model["algorithm"] = item.algorithm
        model["data_create"] = data_create.strftime("%Y-%m-%d %H:%M:%S")
        model["data_update"] = data_update.strftime("%Y-%m-%d %H:%M:%S")
        my_models.append(model)

    db_models = NumbersModelBasicInfo.objects.filter(user_belong=username, delete_status=0)
    for item in db_models:
        model = {}
        data_create = utc2local(item.data_create)
        data_update = utc2local(item.data_update)
        model["cn_name"] = item.cn_name
        model["data_type"] = "数字"
        model["algorithm"] = item.algorithm
        model["data_create"] = data_create.strftime("%Y-%m-%d %H:%M:%S")
        model["data_update"] = data_update.strftime("%Y-%m-%d %H:%M:%S")
        my_models.append(model)

    db_models = ImageModelBasicInfo.objects.filter(user_belong=username, delete_status=0)
    for item in db_models:
        model = {}
        data_create = utc2local(item.data_create)
        data_update = utc2local(item.data_update)
        model["cn_name"] = item.cn_name
        model["data_type"] = "图片"
        model["algorithm"] = item.algorithm
        model["data_create"] = data_create.strftime("%Y-%m-%d %H:%M:%S")
        model["data_update"] = data_update.strftime("%Y-%m-%d %H:%M:%S")
        my_models.append(model)

    try:
        db_teacher = Teacher.objects.get(class_no=class_no)

    except Exception as e:
        return my_models, False

    db_models = TextModelBasicInfo.objects.filter(user_belong=db_teacher.teacher_name, delete_status=0,
                                                  public_status=1, model_type=1)
    for item in db_models:
        model = {}
        data_create = utc2local(item.data_create)
        data_update = utc2local(item.data_update)
        model["teach_name"] = db_teacher.teacher_name
        model["cn_name"] = item.cn_name
        model["data_type"] = "文本"
        model["algorithm"] = item.algorithm
        model["data_create"] = data_create.strftime("%Y-%m-%d %H:%M:%S")
        model["data_update"] = data_update.strftime("%Y-%m-%d %H:%M:%S")
        teach_models.append(model)

    db_models = NumbersModelBasicInfo.objects.filter(user_belong=db_teacher.teacher_name, delete_status=0,
                                                  public_status=1, model_type=1)
    for item in db_models:
        model = {}
        data_create = utc2local(item.data_create)
        data_update = utc2local(item.data_update)
        model["teach_name"] = db_teacher.teacher_name
        model["cn_name"] = item.cn_name
        model["data_type"] = "数字"
        model["algorithm"] = item.algorithm
        model["data_create"] = data_create.strftime("%Y-%m-%d %H:%M:%S")
        model["data_update"] = data_update.strftime("%Y-%m-%d %H:%M:%S")
        teach_models.append(model)

    db_models = ImageModelBasicInfo.objects.filter(user_belong=db_teacher.teacher_name, delete_status=0,
                                                  public_status=1, model_type=1)
    for item in db_models:
        model = {}
        data_create = utc2local(item.data_create)
        data_update = utc2local(item.data_update)
        model["teach_name"] = db_teacher.teacher_name
        model["cn_name"] = item.cn_name
        model["data_type"] = "图片"
        model["algorithm"] = item.algorithm
        model["data_create"] = data_create.strftime("%Y-%m-%d %H:%M:%S")
        model["data_update"] = data_update.strftime("%Y-%m-%d %H:%M:%S")
        teach_models.append(model)

    return my_models, teach_models
