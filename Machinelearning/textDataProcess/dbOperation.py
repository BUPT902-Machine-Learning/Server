# from interaction.models import ModelBasicInfo
# from interaction.models import TrainData as trainDataDB
# from interaction.models import LabelMap
# from interaction.models import ProcessData
# from interaction.models import CNNParams
# from interaction.models import RNNParams
# from users.models import Users
#
#
# def basic_info_save(ch_name, username, algorithm):
#     try:
#         if_exist = ModelBasicInfo.objects.get(user_belong=username, CName=ch_name)
#
#     except Exception as e:
#         if_exist = None
#
#     if if_exist is not None:
#         return
#
#     count = ModelBasicInfo.objects.all().count()
#     en_name = "model" + str(count)
#     user = Users.objects.get(username=username)
#     db_operate = ModelBasicInfo(
#         CName=ch_name,
#         EName=en_name,
#         user_belong=user,
#         algorithm=algorithm
#     )
#     db_operate.save()
#
#
# def basic_info_get(cn_name):
#     response = ModelBasicInfo.objects.get(cn_name=cn_name)
#     if response:
#         return response
#     return "null"
#
#
# def models_get(username):
#     response = ModelBasicInfo.objects.filter(user_belong=username, delete_status=0)
#     return response
#
#
# def models_delete(username, model_name):
#     try:
#         ModelBasicInfo.objects.filter(user_belong=username, CName=model_name).update(delete_status=1)
#
#     except Exception as e:
#         return "delete_error"
#
#     return "delete_confirm"
#
#
# def train_data_save(en_name, db_contents, db_labels):
#     response = trainDataDB.objects.filter(modelName=en_name)
#     if response:
#         trainDataDB.objects.filter(modelName=en_name).update(
#             contents=db_contents,
#             labels=db_labels
#         )
#     else:
#         db_operate = trainDataDB(
#             modelName=en_name,
#             contents=db_contents,
#             labels=db_labels
#         )
#         db_operate.save()
#
#
# def trainDataGet(EName):
#     response = trainDataDB.objects.filter(modelName=EName)
#     contentsAll = response.first().contents
#     labelsAll = response.first().labels
#     return contentsAll, labelsAll
#
#
# def processDataSave(EName, dbContents, dbLabels, data_count, seq_length, classes_count):
#     dbOperate = ProcessData(
#         model_name=EName,
#         contents=dbContents,
#         labels=dbLabels,
#         data_count=data_count,
#         seq_length=seq_length,
#         classes_count=classes_count
#     )
#     dbOperate.save()
#
#
# def processDataGet(EName):
#     response = ProcessData.objects.filter(model_name=EName)
#     seq_length = response.last().seq_length
#     classes_count = response.last().classes_count
#     return seq_length, classes_count
#
#
# def labelTrans(EName, realLabel, convLabel):
#     sep = ';'
#     dbRealLabel = sep.join(realLabel)
#     dbConvLabel = sep.join(convLabel)
#     dbOperate = LabelMap(
#         modelName=EName,
#         realLabel=dbRealLabel,
#         convLabel=dbConvLabel
#     )
#     dbOperate.save()
#
#
# def labels_get(en_name):
#     response = LabelMap.objects.filter(modelName=en_name)
#     labels = response.first()
#     return labels
#
#
# def CNNParamsSet(EName, params):
#     dbOperate = CNNParams(
#         modelName=EName,
#         embeddingDim=params["embedding_dim"],
#         numFilters=params["num_filters"],
#         kernelSize=params["kernel_size"],
#         fullyConnectedDim=params["fully_connected_dim"],
#         dropoutKeepProb=params["dropout_keep_prob"],
#         batchSize=params["batch_size"],
#         numEpochs=params["num_epochs"]
#     )
#     dbOperate.save()
#
#
# def RNNParamsSet(EName, params):
#     dbOperate = RNNParams(
#         modelName=EName,
#         embeddingDim=params["embedding_dim"],
#         numLayers=params["num_layers"],
#         rnn=params["rnn"],
#         hiddenDim=params["hidden_dim"],
#         dropoutKeepProb=params["dropout_keep_prob"],
#         batchSize=params["batch_size"],
#         numEpochs=params["num_epochs"]
#     )
#     dbOperate.save()
#
#
# def CNNParamsGet(EName):
#     response = CNNParams.objects.filter(modelName=EName)
#     params = response.first()
#     return params
#
#
# def RNNParamsGet(EName):
#     response = RNNParams.objects.filter(modelName=EName)
#     params = response.first()
#     return params
