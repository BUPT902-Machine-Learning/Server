import sys

from numbersInteraction.models import NumbersModelBasicInfo, NumbersProcessData
from textDataProcess.interactTrainDataProcess import get_train_data
from textInteraction.models import TextModelBasicInfo, TextProcessData
from imp import reload


if sys.version_info[0] > 2:
    is_py3 = True
else:
    reload(sys)
    sys.setdefaultencoding("utf-8")
    is_py3 = False


def native_content(content):
    if not is_py3:
        return content.decode('utf-8')
    else:
        return content


def transform_labels(raw_train_data):
    labels, train_labels, train_data = [], [], []
    subscript = 0
    for item in raw_train_data:
        try:
            label = item["label"]
            labels.append(native_content(label))
            str_subscript = str(subscript)
            train_labels.append(str_subscript)
            subscript = subscript + 1
            train_data.append(item)

        except:
            pass
    return labels, train_labels, train_data


def max_seq_length(contents):
    max_length = 0
    for item in contents:
        if len(item) > max_length:
            max_length = len(item)
    return max_length


def text_adaptive(data):
    raw_train_data = data["trainData"]
    cn_name = data["modelName"]
    username = data["username"]

    if raw_train_data:
        real_labels, train_labels, train_data = transform_labels(raw_train_data)
        contents, labels = get_train_data(train_data)
        data_count = len(contents)
        seq_length = max_seq_length(contents)

    else:
        try:
            response = TextModelBasicInfo.objects.get(user_belong=username, cn_name=cn_name)
            en_name = response.en_name

        except Exception as e:
            return "请变更训练数据"

        db_operation = TextProcessData.objects.get(model_name=en_name)
        db_train_contents = db_operation.contents
        contents = db_train_contents.split(';')
        data_count = len(contents)
        seq_length = max_seq_length(contents)

    params = dict()
    if data_count <= 20:
        algorithm = "KNN"
        params["k"] = int(data_count / 5) + 1
        data["params"] = params
    elif data_count <= 300:
        algorithm = "CNN"
        batch_size = int(data_count/25) + 1
        num_epochs = int(data_count/batch_size)
        print("www")
        print(batch_size)
        print(num_epochs)
        params["embedding_dim"] = '-1'
        params["num_filters"] = '-1'
        params["kernel_size"] = '-1'
        params["fully_connected_dim"] = '-1'
        params["dropout_keep_prob"] = '-1'
        params["batch_size"] = batch_size
        params["num_epochs"] = num_epochs
        data["params"] = params

    else:
        algorithm = "RNN"
        batch_size = int(data_count / 50) + 1
        num_epochs = data_count / batch_size
        params["embedding_dim"] = '-1'
        params["num_layers"] = '-1'
        params["rnn_type"] = '0'
        params["hidden_dim"] = '-1'
        params["dropout_keep_prob"] = '-1'
        params["batch_size"] = batch_size
        params["num_epochs"] = num_epochs
        data["params"] = params

    return algorithm, data


def numbers_adaptive(data):
    raw_train_data = data["trainData"]
    cn_name = data["modelName"]
    username = data["username"]
    value_data = data["valueData"]

    if raw_train_data:
        real_labels, train_labels, train_data = transform_labels(raw_train_data)
        contents, labels = get_train_data(train_data)
        data_count = len(contents)
        seq_length = len(value_data)

    else:
        try:
            response = NumbersModelBasicInfo.objects.get(user_belong=username, cn_name=cn_name)
            en_name = response.en_name

        except Exception as e:
            return "请变更训练数据"

        db_operation = NumbersProcessData.objects.get(model_name=en_name)
        db_train_contents = db_operation.contents
        contents = db_train_contents.split(';')
        data_count = len(contents)
        seq_length = max_seq_length(contents)

    params = dict()
    if data_count <= 20 and seq_length < 20:
        algorithm = "KNN"
        params["k"] = int(seq_length / 5) + 1
        data["params"] = params
    elif data_count <= 600:
        algorithm = "CNN"
    else:
        algorithm = "RNN"
    return algorithm, data
