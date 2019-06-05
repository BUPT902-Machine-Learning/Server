# encoding: utf-8
import os
import sys
import time
import datetime
import textCoreAlgorithm.algorithm_KNN.run_knn as run_knn
import textCoreAlgorithm.algorithm_CNN.run_cnn as run_cnn
import textCoreAlgorithm.algorithm_RNN.run_rnn as run_rnn
# import textCoreAlgorithm.a lgorithm_SVM.adaptive_run_knn as adaptive_run_svm
# import textCoreAlgorithm.algorithm_KNN.adaptive_run_knn as adaptive_run_knn
# import textCoreAlgorithm.algorithm_CNN.adaptive_run_cnn as adaptive_run_cnn
# import textCoreAlgorithm.algorithm_RNN.adaptive_run_rnn as adaptive_run_rnn
# from textCoreAlgorithm.algorithm_CNN.cnn_model import TCNNConfig
# from textCoreAlgorithm.algorithm_RNN.rnn_model import TRNNConfig
from cooperation.models import TextCooperationModels
from textDataProcess.paramsSet import cnn_set, rnn_set, test_cnn_set, test_rnn_set
from textInteraction.models import Users, TextModelBasicInfo, TextLabelMap, TextTrainData, TextProcessData, TextCNNParams, TextRNNParams, TextKNNParams
from textDataProcess.dataload import build_vocab
from imp import reload

if sys.version_info[0] > 2:
    is_py3 = True
else:
    reload(sys)
    sys.setdefaultencoding("utf-8")
    is_py3 = False


def get_time_dif(start_time):
    """获取已使用时间"""
    end_time = time.time()
    time_dif = end_time - start_time
    return datetime.timedelta(seconds=int(round(time_dif)))


def transform_labels(raw_train_data):
    labels, train_labels, train_data = [], [], []
    subscript = 0
    for item in raw_train_data:
        try:
            label = item["label"]
            labels.append(native_content(label))
            str_subscript = str(subscript)
            train_labels.append(str_subscript)
            item2 = item.copy()
            item2["label"] = str_subscript
            subscript = subscript + 1
            train_data.append(item2)

        except:
            pass
    return labels, train_labels, train_data


def get_train_data(train_data):
    contents, labels = [], []

    for item in train_data:
        try:
            label = item["label"]
            for content in item["contents"]:
                contents.append(native_content(content))
                labels.append(native_content(label))

        except:
            pass

    return contents, labels


def get_all_data(content_all, label_all):
    contents, labels = [], []
    for label, content in zip(label_all, content_all):
        contents.append(list(native_content(content)))
        labels.append(native_content(label))
    return contents, labels


def max_seq_length(contents):
    max_length = 0
    for item in contents:
        if len(item) > max_length:
            max_length = len(item)
    return max_length


def knn_train_data(raw_data):
    raw_train_data = raw_data["trainData"]
    cn_name = raw_data["modelName"]
    username = raw_data["username"]
    model_type = raw_data["model_type"]
    public_status = raw_data["public_status"]
    params = raw_data["params"]
    k = int(params["k"])
    if k == -1:
        k = 3

    try:
        response = TextModelBasicInfo.objects.get(user_belong=username, cn_name=cn_name)
        en_name = response.en_name

    except Exception as e:
        count = TextModelBasicInfo.objects.all().count()
        en_name = "model" + str(count)
        user = Users.objects.get(username=username)
        db_operate = TextModelBasicInfo(
            cn_name=cn_name,
            en_name=en_name,
            user_belong=user,
            public_status=public_status,
            model_type=model_type,
            algorithm="KNN"
        )
        db_operate.save()
        response = TextModelBasicInfo.objects.get(en_name=en_name)

    save_dir = 'checkpoints/' + username + '/textModels/' + en_name

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    if raw_train_data:
        real_labels, train_labels, train_data = transform_labels(raw_train_data)
        separator = ';'
        db_real_labels = separator.join(real_labels)
        db_train_labels = separator.join(train_labels)
        try:
            TextLabelMap.objects.get(model_name=en_name)
            TextLabelMap.objects.filter(model_name=en_name).update(
                real_labels=db_real_labels,
                train_labels=db_train_labels
            )

        except Exception as e:
            db_operation = TextLabelMap(
                model_name=response,
                real_labels=db_real_labels,
                train_labels=db_train_labels
            )
            db_operation.save()

        contents, labels = get_train_data(train_data)
        db_labels = separator.join(labels)
        db_data = separator.join(contents)
        db_operation = TextTrainData(
            model_name=response,
            contents=db_data,
            labels=db_labels
        )
        db_operation.save()
        data_count = len(contents)
        classes_count = len(train_labels)
        seq_length = max_seq_length(contents)

        try:
            TextProcessData.objects.get(model_name=en_name)
            TextProcessData.objects.filter(model_name=en_name).update(
                contents=db_data,
                labels=db_labels,
                data_count=data_count,
                seq_length=seq_length,
                classes_count=classes_count
            )

        except Exception as e:
            db_operation = TextProcessData(
                model_name=response,
                contents=db_data,
                labels=db_labels,
                data_count=data_count,
                seq_length=seq_length,
                classes_count=classes_count
            )
            db_operation.save()

    else:
        db_operation = TextProcessData.objects.get(model_name=en_name)
        db_train_contents = db_operation.contents
        contents = db_train_contents.split(';')

        db_real_labels = db_operation.labels
        labels = db_real_labels.split(';')

    try:
        TextKNNParams.objects.get(model_name=en_name)
        TextKNNParams.objects.filter(model_name=en_name).update(
            k=k
        )
    except Exception as e:
        db_operation = TextKNNParams(
            model_name=response,
            k=k
        )
        db_operation.save()

    print(contents)
    print(labels)
    acc, time_c = run_knn.train(contents, labels, save_dir, k)
    TextModelBasicInfo.objects.filter(en_name=en_name).update(
        accuracy=acc,
        public_status=public_status,
        algorithm="KNN",

    )
    return acc, time_c


def cnn_train_data(raw_data):
    raw_train_data = raw_data["trainData"]
    cn_name = raw_data["modelName"]
    username = raw_data["username"]
    model_type = raw_data["model_type"]
    public_status = raw_data["public_status"]
    params = raw_data["params"]

    try:
        response = TextModelBasicInfo.objects.get(user_belong=username, cn_name=cn_name)
        en_name = response.en_name

    except Exception as e:
        count = TextModelBasicInfo.objects.all().count()
        en_name = "model" + str(count)
        user = Users.objects.get(username=username)
        db_operate = TextModelBasicInfo(
            cn_name=cn_name,
            en_name=en_name,
            user_belong=user,
            public_status=public_status,
            model_type=model_type,
            algorithm="CNN"
        )
        db_operate.save()
        response = TextModelBasicInfo.objects.get(en_name=en_name)

    save_dir = 'checkpoints/' + username + '/textModels/' + en_name
    vocab_dir = 'data/modelVocabs/' + username + '/textModels/'
    vocab_dir_txt = vocab_dir + en_name + 'Vocab.txt'

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    if not os.path.exists(vocab_dir):
        os.makedirs(vocab_dir)

    if raw_train_data:
        real_labels, train_labels, train_data = transform_labels(raw_train_data)
        separator = ';'
        db_real_labels = separator.join(real_labels)
        db_train_labels = separator.join(train_labels)
        try:
            TextLabelMap.objects.get(model_name=en_name)
            TextLabelMap.objects.filter(model_name=en_name).update(
                real_labels=db_real_labels,
                train_labels=db_train_labels
            )

        except Exception as e:
            db_operation = TextLabelMap(
                model_name=response,
                real_labels=db_real_labels,
                train_labels=db_train_labels
            )
            db_operation.save()

        contents, labels = get_train_data(train_data)
        train_contents = build_vocab(contents, vocab_dir_txt, 5000)
        participle = '|'
        db_labels = separator.join(labels)
        db_data = separator.join(contents)
        db_contents = []
        for item in train_contents:
            db_content = participle.join(item)
            db_contents.append(db_content)

        db_train_contents = separator.join(db_contents)
        db_operation = TextTrainData(
            model_name=response,
            contents=db_data,
            labels=db_labels
        )
        db_operation.save()
        data_count = len(contents)
        classes_count = len(train_labels)
        seq_length = max_seq_length(contents)
        params["num_classes"] = classes_count
        params["seq_length"] = seq_length

        try:
            TextProcessData.objects.get(model_name=en_name)
            TextProcessData.objects.filter(model_name=en_name).update(
                contents=db_train_contents,
                labels=db_labels,
                data_count=data_count,
                seq_length=seq_length,
                classes_count=classes_count
            )

        except Exception as e:
            db_operation = TextProcessData(
                model_name=response,
                contents=db_train_contents,
                labels=db_labels,
                data_count=data_count,
                seq_length=seq_length,
                classes_count=classes_count
            )
            db_operation.save()

    else:
        db_operation = TextProcessData.objects.get(model_name=en_name)
        params["num_classes"] = db_operation.classes_count
        params["seq_length"] = db_operation.seq_length
        db_train_contents = db_operation.contents
        db_contents = db_train_contents.split(';')
        train_contents = []
        for item in db_contents:
            train_content = item.split('|')
            train_contents.append(train_content)

        db_real_labels = db_operation.labels
        labels = db_real_labels.split(';')
        db_operation = TextLabelMap.objects.get(model_name=en_name)
        train_labels = db_operation.train_labels.split(';')

    config = cnn_set(params)
    try:
        TextCNNParams.objects.get(model_name=en_name)
        TextCNNParams.objects.filter(model_name=en_name).update(
            embedding_dim=params["embedding_dim"],
            num_filters=params["num_filters"],
            kernel_size=params["kernel_size"],
            fully_connected_dim=params["fully_connected_dim"],
            dropout_keep_prob=params["dropout_keep_prob"],
            batch_size=params["batch_size"],
            num_epochs=params["num_epochs"]
        )
    except Exception as e:
        db_operation = TextCNNParams(
            model_name=response,
            embedding_dim=params["embedding_dim"],
            num_filters=params["num_filters"],
            kernel_size=params["kernel_size"],
            fully_connected_dim=params["fully_connected_dim"],
            dropout_keep_prob=params["dropout_keep_prob"],
            batch_size=params["batch_size"],
            num_epochs=params["num_epochs"]
        )
        db_operation.save()

    loss1, acc, time_c = run_cnn.train(config, train_contents, train_labels, labels, save_dir, vocab_dir_txt)
    loss = round(loss1, 4)
    TextModelBasicInfo.objects.filter(en_name=en_name).update(
        accuracy=acc,
        loss=loss,
        public_status=public_status,
        algorithm="CNN"
    )
    return loss, acc, time_c


def rnn_train_data(raw_data):
    raw_train_data = raw_data["trainData"]
    cn_name = raw_data["modelName"]
    username = raw_data["username"]
    model_type = raw_data["model_type"]
    public_status = raw_data["public_status"]
    params = raw_data["params"]

    try:
        response = TextModelBasicInfo.objects.get(user_belong=username, cn_name=cn_name)
        en_name = response.en_name

    except Exception as e:
        count = TextModelBasicInfo.objects.all().count()
        en_name = "model" + str(count)
        user = Users.objects.get(username=username)
        db_operate = TextModelBasicInfo(
            cn_name=cn_name,
            en_name=en_name,
            user_belong=user,
            public_status=public_status,
            model_type=model_type,
            algorithm="RNN"
        )
        db_operate.save()
        response = TextModelBasicInfo.objects.get(en_name=en_name)

    save_dir = 'checkpoints/' + username + '/textModels/' + en_name
    vocab_dir = 'data/modelVocabs/' + username
    vocab_dir_txt = vocab_dir + '/textModels/' + en_name + 'Vocab.txt'

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    if not os.path.exists(vocab_dir):
        os.makedirs(vocab_dir)

    if raw_train_data:
        real_labels, train_labels, train_data = transform_labels(raw_train_data)
        separator = ';'
        db_real_labels = separator.join(real_labels)
        db_train_labels = separator.join(train_labels)
        try:
            TextLabelMap.objects.get(model_name=en_name)
            TextLabelMap.objects.filter(model_name=en_name).update(
                real_labels=db_real_labels,
                train_labels=db_train_labels
            )

        except Exception as e:
            db_operation = TextLabelMap(
                model_name=response,
                real_labels=db_real_labels,
                train_labels=db_train_labels
            )
            db_operation.save()

        contents, labels = get_train_data(train_data)
        train_contents = build_vocab(contents, vocab_dir_txt, 5000)
        participle = '|'
        db_labels = separator.join(labels)
        db_data = separator.join(contents)
        db_contents = []
        for item in train_contents:
            db_content = participle.join(item)
            db_contents.append(db_content)

        db_train_contents = separator.join(db_contents)
        db_operation = TextTrainData(
            model_name=response,
            contents=db_data,
            labels=db_labels
        )
        db_operation.save()
        data_count = len(contents)
        classes_count = len(train_labels)
        seq_length = max_seq_length(contents)
        params["num_classes"] = classes_count
        params["seq_length"] = seq_length

        try:
            TextProcessData.objects.get(model_name=en_name)
            TextProcessData.objects.filter(model_name=en_name).update(
                contents=db_train_contents,
                labels=db_labels,
                data_count=data_count,
                seq_length=seq_length,
                classes_count=classes_count
            )

        except Exception as e:
            db_operation = TextProcessData(
                model_name=response,
                contents=db_train_contents,
                labels=db_labels,
                data_count=data_count,
                seq_length=seq_length,
                classes_count=classes_count
            )
            db_operation.save()

    else:
        db_operation = TextProcessData.objects.get(model_name=en_name)
        params["num_classes"] = db_operation.classes_count
        params["seq_length"] = db_operation.seq_length
        db_train_contents = db_operation.contents
        db_contents = db_train_contents.split(';')
        train_contents = []
        for item in db_contents:
            train_content = item.split('|')
            train_contents.append(train_content)

        db_real_labels = db_operation.labels
        labels = db_real_labels.split(';')
        db_operation = TextLabelMap.objects.get(model_name=en_name)
        train_labels = db_operation.train_labels.split(';')

    config = rnn_set(params)
    try:
        TextRNNParams.objects.get(model_name=en_name)
        TextRNNParams.objects.filter(model_name=en_name).update(
            embedding_dim=params["embedding_dim"],
            num_layers=params["num_layers"],
            rnn_type=params["rnn_type"],
            hidden_dim=params["hidden_dim"],
            dropout_keep_prob=params["dropout_keep_prob"],
            batch_size=params["batch_size"],
            num_epochs=params["num_epochs"]
        )
    except Exception as e:
        db_operation = TextRNNParams(
            model_name=response,
            embedding_dim=params["embedding_dim"],
            num_layers=params["num_layers"],
            rnn_type=params["rnn_type"],
            hidden_dim=params["hidden_dim"],
            dropout_keep_prob=params["dropout_keep_prob"],
            batch_size=params["batch_size"],
            num_epochs=params["num_epochs"]
        )
        db_operation.save()

    loss1, acc, time_c = run_rnn.train(config, train_contents, train_labels, labels, save_dir, vocab_dir_txt)
    loss = round(loss1, 4)
    TextModelBasicInfo.objects.filter(en_name=en_name).update(
        accuracy=acc,
        loss=loss,
        public_status=public_status,
        algorithm="RNN"
    )
    return loss, acc, time_c


def native_content(content):
    if not is_py3:
        return content.decode('utf-8')
    else:
        return content
