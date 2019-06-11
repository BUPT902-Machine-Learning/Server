import textCoreAlgorithm.algorithm_CNN.run_cnn as run_cnn
from textCoreAlgorithm.algorithm_KNN import run_knn
from textDataProcess.paramsSet import cnn_set, rnn_set, test_cnn_set, test_rnn_set
from textInteraction.models import Users, TextModelBasicInfo, TextLabelMap, TextTrainData, TextProcessData, TextCNNParams


def get_models(username):
    models = []
    db_models = TextModelBasicInfo.objects.filter(user_belong=username, delete_status=0)
    for item in db_models:
        model = {}
        model["cn_name"] = item.cn_name
        model["algorithm"] = item.algorithm
        models.append(model)

    return models


def get_labels(username, cn_name):
    response = TextModelBasicInfo.objects.get(user_belong=username, cn_name=cn_name, delete_status=0)
    en_name = response.en_name
    db_labels = TextLabelMap.objects.get(model_name=en_name)
    labels = db_labels.real_labels.split(';')
    return labels


def test_data_process(raw_data):
    test_data = raw_data["testData"]
    cn_name = raw_data["modelName"]
    username = raw_data["username"]
    response = TextModelBasicInfo.objects.get(cn_name=cn_name)
    en_name = response.en_name
    algorithm = response.algorithm

    if test_data:
        content = test_data
        response = TextLabelMap.objects.get(model_name=en_name)
        real_labels = response.real_labels.split(';')
        train_labels = response.train_labels.split(';')
        response = TextProcessData.objects.filter(model_name=en_name)
        seq_length = response.last().seq_length
        classes_count = response.last().classes_count

        # if algorithm == 'KNN':
        #     dbContents, dbLabels = dbOperation.trainDataGet(EName)
        #     contentsAll = dbContents.split(';')
        #     contentsAll.append(content)
        #     numPrediction, time = run_knn.test(contentsAll, EName)

        if algorithm == 'CNN':
            response = TextCNNParams.objects.get(model_name=en_name)
            params = response
            params.classes_count = classes_count
            params.seq_length = seq_length
            config = test_cnn_set(params)
            num_prediction, time = run_cnn.test(config, train_labels, content, en_name)

        elif algorithm == 'KNN':
            response = TextModelBasicInfo.objects.get(user_belong=username, cn_name=cn_name, delete_status=0)
            en_name = response.en_name
            save_dir = 'checkpoints/' + username + '/textModels/' + en_name
            response = TextLabelMap.objects.get(model_name=en_name)
            real_labels = response.real_labels.split(';')
            num_prediction, time = run_knn.test(test_data, save_dir)

            num_prediction = real_labels[int(num_prediction)]
            return num_prediction, time

        # elif algorithm == 'RNN':
        #     params = dbOperation.RNNParamsGet(EName)
        #     params.classes_count = classes_count
        #     params.seq_length = seq_length
        #     config = testRNNSet(params)
        #     numPrediction, time = run_rnn.test(config, convLabels, content, EName)

        print(num_prediction)
        prediction = real_labels[int(num_prediction)]
        return prediction, time


