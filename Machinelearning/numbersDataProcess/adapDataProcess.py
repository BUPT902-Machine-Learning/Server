# encoding: utf-8
import sys
import textCoreAlgorithm.algorithm_KNN.run_knn as run_knn
import textCoreAlgorithm.algorithm_CNN.run_cnn as run_cnn
import textCoreAlgorithm.algorithm_RNN.run_rnn as run_rnn
import textDataProcess.dbOperation as dbOperation
from textDataProcess.paramsSet import CNNSet, RNNSet, testCNNSet, testRNNSet
from imp import reload

if sys.version_info[0] > 2:
    is_py3 = True
else:
    reload(sys)
    sys.setdefaultencoding("utf-8")
    is_py3 = False


def sepLabels(rowTrainData):
    labels, convLabel, trainData = [], [], []
    subscript = 0
    for item in rowTrainData:
        try:
            label = item["label"]
            labels.append(native_content(label))
            strSubscript = str(subscript)
            convLabel.append(strSubscript)
            item["label"] = strSubscript
            subscript = subscript + 1
            trainData.append(item)

        except:
            pass
    return labels, convLabel, trainData


def sepFirstData(trainData):
    contents, labels = [], []

    for item in trainData:
        try:
            label = item["label"]
            for content in item["contents"]:
                contents.append(native_content(content))
                labels.append(native_content(label))

        except:
            pass

    return contents, labels


def sepSecondData(contentsAll, labelsAll):
    contents, labels = [], []
    for label, content in zip(labelsAll, contentsAll):
        contents.append(list(native_content(content)))
        labels.append(native_content(label))
    return contents, labels


def maxSeqLength(contents):
    max_length = 0
    for item in contents:
        if len(item) > max_length:
            max_length = len(item)
    return max_length


def trainDataProcess(rowData):
    try:
        rowTrainData = rowData["traindata"]

    except:
        return
    modelCName = rowData["modelName"]
    params = rowData["params"]
    algorithm = params["algoSelect"]
    dbOperation.basicInforSave(modelCName, algorithm)
    basicInfor = dbOperation.basicInforGet(modelCName)
    EName = basicInfor.EName

    if rowTrainData:
        ifTraindata = True
        realLabels, convLabel, trainData = sepLabels(rowTrainData)
        dbOperation.labelTrans(EName, realLabels, convLabel)
        contentsAll, labelsAll = sepFirstData(trainData)
        sep = ';'
        dbContents = sep.join(contentsAll)
        dbLabels = sep.join(labelsAll)
        dbOperation.trainDataSave(EName, dbContents, dbLabels)
        contents, labels = sepSecondData(contentsAll, labelsAll)
        data_count = len(contents)
        classes_count = len(convLabel)
        seq_length = maxSeqLength(contents)
        dbOperation.processDataSave(EName, dbContents, dbLabels, data_count, seq_length, classes_count)

    else:
        ifTraindata = False
        dbContents, dbLabels = dbOperation.trainDataGet(EName)
        contentsAll = dbContents.split(';')
        labelsAll = dbLabels.split(';')
        contents, labels = sepSecondData(contentsAll, labelsAll)

    dbLabels = dbOperation.labels_get(EName)
    convLabels = dbLabels.convLabel.split(';')

    if algorithm == 'KNN':
        loss1, acc, time = run_knn.train(contentsAll, labelsAll, EName)
        return loss1, acc, time

    elif algorithm == 'CNN':
        params["num_classes"] = len(convLabels)
        params["seq_length"] = maxSeqLength(contents)
        config = CNNSet(params)
        dbOperation.CNNParamsSet(EName, params)
        loss1, acc, time = run_cnn.train(config, ifTraindata, convLabels, contents, labels, EName)
        loss = round(loss1, 4)
        return loss, acc, time

    elif algorithm == 'RNN':
        params["num_classes"] = len(convLabels)
        params["seq_length"] = maxSeqLength(contents)
        config = RNNSet(params)
        dbOperation.RNNParamsSet(EName, params)
        loss1, acc, time = run_rnn.train(config, ifTraindata, convLabels, contents, labels, EName)
        loss = round(loss1, 4)
        return loss, acc, time

    elif algorithm == 'SVM':
        print("4")


def testDataProcess(rowData):
    modelCName = rowData["modelName"]
    basicInfor = dbOperation.basicInforGet(modelCName)
    EName = basicInfor.EName
    algorithm = basicInfor.algorithm

    if EName == "null":
        return "null", "null"

    try:
        testData = rowData["testdata"]

    except:
        return

    if testData:
        content = testData
        dbLabels = dbOperation.labels_get(EName)
        realLabels = dbLabels.realLabel.split(';')
        convLabels = dbLabels.convLabel.split(';')
        seq_length, classes_count = dbOperation.processDataGet(EName)

        if algorithm == 'KNN':
            dbContents, dbLabels = dbOperation.trainDataGet(EName)
            contentsAll = dbContents.split(';')
            contentsAll.append(content)
            numPrediction, time = run_knn.test(contentsAll, EName)

        elif algorithm == 'CNN':
            params = dbOperation.CNNParamsGet(EName)
            params.classes_count = classes_count
            params.seq_length = seq_length
            config = testCNNSet(params)
            numPrediction, time = run_cnn.test(config, convLabels, content, EName)

        elif algorithm == 'RNN':
            params = dbOperation.RNNParamsGet(EName)
            params.classes_count = classes_count
            params.seq_length = seq_length
            config = testRNNSet(params)
            numPrediction, time = run_rnn.test(config, convLabels, content, EName)

        print(numPrediction)
        prediction = realLabels[int(numPrediction)]
        return prediction, time


def native_content(content):
    if not is_py3:
        return content.decode('utf-8')
    else:
        return content