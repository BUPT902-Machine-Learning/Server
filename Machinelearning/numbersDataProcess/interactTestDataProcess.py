import numbersCoreAlgorithm.algorithm_KNN.run_knn as run_knn
from numbersInteraction.models import NumbersModelBasicInfo, NumbersLabelMap


def knn_test_data(raw_data):
    test_data = raw_data["test_data"]
    cn_name = raw_data["model_name"]
    username = raw_data["username"]
    response = NumbersModelBasicInfo.objects.get(user_belong=username, cn_name=cn_name)
    en_name = response.en_name

    save_dir = 'checkpoints/' + username + '/numbersModels/' + en_name

    if test_data:
        response = NumbersLabelMap.objects.get(model_name=en_name)
        real_labels = response.real_labels.split(';')
        num_prediction, time = run_knn.test(test_data, save_dir)

        prediction = real_labels[int(num_prediction)]
        return prediction, time


# def cnn_test_data(raw_data):
#     test_data = raw_data["testData"]
#     cn_name = raw_data["modelName"]
#     username = raw_data["username"]
#     response = NumbersModelBasicInfo.objects.get(user_belong=username, cn_name=cn_name)
#     en_name = response.en_name
#
#     save_dir = 'checkpoints/' + username + '/numbersModels/' + en_name
#     vocab_dir = 'data/modelVocabs/' + username
#     vocab_dir_txt = vocab_dir + '/numbersModels/' + en_name + 'Vocab.txt'
#
#     if test_data:
#         content = participle_test_data(test_data)
#         response = NumbersLabelMap.objects.get(model_name=en_name)
#         real_labels = response.real_labels.split(';')
#         response = NumbersProcessData.objects.get(model_name=en_name)
#         seq_length = response.seq_length
#         classes_count = response.classes_count
#
#         response = NumbersCNNParams.objects.get(model_name=en_name)
#         params = response
#         params.classes_count = classes_count
#         params.seq_length = seq_length
#         config = test_cnn_set(params)
#         num_prediction, time = run_cnn.test(config, content, save_dir, vocab_dir_txt)
#
#         prediction = real_labels[int(num_prediction)]
#         return prediction, time
#
#
# def rnn_test_data(raw_data):
#     test_data = raw_data["testData"]
#     cn_name = raw_data["modelName"]
#     username = raw_data["username"]
#     response = NumbersModelBasicInfo.objects.get(user_belong=username, cn_name=cn_name)
#     en_name = response.en_name
#
#     save_dir = 'checkpoints/' + username + '/numbersModels/' + en_name
#     vocab_dir = 'data/modelVocabs/' + username
#     vocab_dir_txt = vocab_dir + '/numbersModels/' + en_name + 'Vocab.txt'
#
#     if test_data:
#         content = participle_test_data(test_data)
#         response = NumbersLabelMap.objects.get(model_name=en_name)
#         real_labels = response.real_labels.split(';')
#         response = NumbersProcessData.objects.get(model_name=en_name)
#         seq_length = response.seq_length
#         classes_count = response.classes_count
#
#         response = NumbersRNNParams.objects.get(model_name=en_name)
#         params = response
#         params.classes_count = classes_count
#         params.seq_length = seq_length
#         config = test_rnn_set(params)
#         num_prediction, time = run_rnn.test(config, content, save_dir, vocab_dir_txt)
#
#         prediction = real_labels[int(num_prediction)]
#         return prediction, time
