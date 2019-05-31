from rest_framework.response import Response
from rest_framework.decorators import api_view
from adaptive.adaptiveProcess import text_adaptive, numbers_adaptive
import textDataProcess.interactTrainDataProcess as textTrainDataProcess
import numbersDataProcess.interactTrainDataProcess as numbersTrainDataProcess


class API:
    @api_view(['GET', 'POST'])
    def text_train(request, format=None):
        if request.method == 'GET':
            print("GET")
            return Response()

        elif request.method == 'POST':
            print("POST")
            print(request.data)
            data = request.data
            algorithm, data = text_adaptive(data)
            print(data)
            if algorithm == "KNN":
                k = data["params"]["k"]
                acc, time = textTrainDataProcess.knn_train_data(data)
                while acc < 0.85 and k > 1:
                    data["params"]["k"] -= 1
                    k = data["params"]["k"]
                    acc, time = textTrainDataProcess.knn_train_data(data)

            elif algorithm == "CNN":
                loss, acc, time = textTrainDataProcess.cnn_train_data(data)
            elif algorithm == "RNN":
                loss, acc, time = textTrainDataProcess.rnn_train_data(data)

            return Response({
                "acc": acc,
                "time": time
            })

    @api_view(['GET', 'POST'])
    def numbers_train(request, format=None):
        if request.method == 'GET':
            print("GET")
            return Response()

        elif request.method == 'POST':
            print("POST")
            print(request.data)
            data = request.data
            print(data["trainData"])
            algorithm, data = numbers_adaptive(data)
            if algorithm == "KNN":
                k = data["params"]["k"]
                acc, time = numbersTrainDataProcess.knn_train_data(data)
                while acc < 0.85 and k > 1:
                    data["params"]["k"] -= 1
                    k = data["params"]["k"]
                    acc, time = numbersTrainDataProcess.knn_train_data(data)
            #
            # elif algorithm == "CNN":
            #     loss, acc, time = cnn_train_data(data)
            # elif algorithm == "RNN":
            #     loss, acc, time = rnn_train_data(data)

            return Response({
                "acc": acc,
                "time": time
            })
#
#     @api_view(['GET', 'POST'])
#     def testdata(request, format=None):
#         if request.method == 'GET':
#             print("GET")
#             return Response()
#
#         elif request.method == 'POST':
#             print("POST")
#             print(request.data)
#             rowData = request.data
#             KNN, CNN, RNN, time = adaptiveTestData(rowData)
#             return Response({
#                 "KNN": KNN,
#                 "CNN": CNN,
#                 "RNN": RNN,
#                 "time": time
#             })
