import textCoreAlgorithm.algorithm_KNN.run_knn as run_knn
import textCoreAlgorithm.algorithm_CNN.run_cnn as run_cnn
import textCoreAlgorithm.algorithm_RNN.run_rnn as run_rnn
from textInteraction.models import TextModelBasicInfo, TextLabelMap, TextProcessData, TextCNNParams, TextRNNParams
from textDataProcess.paramsSet import test_cnn_set, test_rnn_set
from textDataProcess.dataload import participle_test_data


def knn_test_data(raw_data):
    test_data = raw_data["testData"]
    cn_name = raw_data["modelName"]
    username = raw_data["username"]
    response = TextModelBasicInfo.objects.get(user_belong=username, cn_name=cn_name)
    en_name = response.en_name

    save_dir = 'checkpoints/' + username + '/textModels/' + en_name

    if test_data:
        response = TextLabelMap.objects.get(model_name=en_name)
        real_labels = response.real_labels.split(';')
        num_prediction, time = run_knn.test(test_data, save_dir)

        prediction = real_labels[int(num_prediction)]
        return prediction, time


def cnn_test_data(raw_data):
    test_data = raw_data["testData"]
    cn_name = raw_data["modelName"]
    username = raw_data["username"]
    response = TextModelBasicInfo.objects.get(user_belong=username, cn_name=cn_name)
    en_name = response.en_name

    save_dir = 'checkpoints/' + username + '/textModels/' + en_name
    vocab_dir = 'data/modelVocabs/' + username + '/textModels/'
    vocab_dir_txt = vocab_dir + en_name + 'Vocab.txt'

    if test_data:
        content = participle_test_data(test_data)
        response = TextLabelMap.objects.get(model_name=en_name)
        real_labels = response.real_labels.split(';')
        response = TextProcessData.objects.get(model_name=en_name)
        seq_length = response.seq_length
        classes_count = response.classes_count

        response = TextCNNParams.objects.get(model_name=en_name)
        params = response
        params.classes_count = classes_count
        params.seq_length = seq_length
        config = test_cnn_set(params)
        num_prediction, time = run_cnn.test(config, content, save_dir, vocab_dir_txt)

        prediction = real_labels[int(num_prediction)]
        return prediction, time


def rnn_test_data(raw_data):
    test_data = raw_data["testData"]
    cn_name = raw_data["modelName"]
    username = raw_data["username"]
    response = TextModelBasicInfo.objects.get(user_belong=username, cn_name=cn_name)
    en_name = response.en_name

    save_dir = 'checkpoints/' + username + '/textModels/' + en_name
    vocab_dir = 'data/modelVocabs/' + username + '/textModels/'
    vocab_dir_txt = vocab_dir + en_name + 'Vocab.txt'

    if test_data:
        content = participle_test_data(test_data)
        response = TextLabelMap.objects.get(model_name=en_name)
        real_labels = response.real_labels.split(';')
        response = TextProcessData.objects.get(model_name=en_name)
        seq_length = response.seq_length
        classes_count = response.classes_count

        response = TextRNNParams.objects.get(model_name=en_name)
        params = response
        params.classes_count = classes_count
        params.seq_length = seq_length
        config = test_rnn_set(params)
        num_prediction, time = run_rnn.test(config, content, save_dir, vocab_dir_txt)

        prediction = real_labels[int(num_prediction)]
        return prediction, time
