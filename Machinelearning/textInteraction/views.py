from rest_framework.response import Response

from cooperation.models import TextCooperationModels
from textDataProcess.interactTrainDataProcess import knn_train_data, cnn_train_data, rnn_train_data
from textDataProcess.interactTestDataProcess import knn_test_data, cnn_test_data, rnn_test_data
from rest_framework.decorators import api_view

from textInteraction.models import TextModelBasicInfo


class API:
    # classInfo SVMAPI:
    #     @api_view(['GET', 'POST'])
    #     def trainData(request, format=None):
    #         if request.method == 'GET':
    #             print("GET")
    #             return Response()
    #
    #         elif request.method == 'POST':
    #             print("POST")
    #             print(request.data)
    #             rawData = request.data
    #             loss, acc, time = SVMTrainData(rawData)
    #             return Response({
    #                 "loss": loss,
    #                 "acc": acc,
    #                 "time": time
    #             })
    #
    #     @api_view(['GET', 'POST'])
    #     def testData(request, format=None):
    #         if request.method == 'GET':
    #             print("GET")
    #             return Response()
    #
    #         elif request.method == 'POST':
    #             print("POST")
    #             print(request.data)
    #             rowdata = request.data
    #             prediction, time = SVMTestData(rowdata)
    #             if prediction == "null":
    #                 return Response("null")
    #             return Response({
    #                 "prediction": prediction,
    #                 "time": time
    #             })

    class KnnAPI:
        @api_view(['GET', 'POST'])
        def train_data(request, format=None):
            if request.method == 'GET':
                print("GET")
                return Response()

            elif request.method == 'POST':
                print("POST")
                print(request.data)
                raw_data = request.data
                acc, time = knn_train_data(raw_data)
                return Response({
                    "acc": acc,
                    "time": time
                })

        @api_view(['GET', 'POST'])
        def test_data(request, format=None):
            if request.method == 'GET':
                print("GET")
                return Response()

            elif request.method == 'POST':
                print("POST")
                print(request.data)
                data = request.data
                prediction, time = knn_test_data(data)
                if prediction == "null":
                    return Response("预测结果错误，请重试！")
                return Response({
                    "prediction": prediction,
                    "time": time
                })

    class CnnAPI:
        @api_view(['GET', 'POST'])
        def train_data(request, format=None):
            if request.method == 'GET':
                print("GET")
                return Response()

            elif request.method == 'POST':
                print("POST")
                print(request.data)
                raw_data = request.data
                loss, acc, time = cnn_train_data(raw_data)
                return Response({
                    "loss": loss,
                    "acc": acc,
                    "time": time
                })

        @api_view(['GET', 'POST'])
        def test_data(request, format=None):
            if request.method == 'GET':
                print("GET")
                return Response()

            elif request.method == 'POST':
                print("POST")
                print(request.data)
                data = request.data
                prediction, time = cnn_test_data(data)
                if prediction == "null":
                    return Response("预测结果错误，请重试！")
                return Response({
                    "prediction": prediction,
                    "time": time
                })

    class RnnAPI:
        @api_view(['GET', 'POST'])
        def train_data(request, format=None):
            if request.method == 'GET':
                print("GET")
                return Response()

            elif request.method == 'POST':
                print("POST")
                print(request.data)
                raw_data = request.data

                loss, acc, time = rnn_train_data(raw_data)
                return Response({
                    "loss": loss,
                    "acc": acc,
                    "time": time
                })

        @api_view(['GET', 'POST'])
        def test_data(request, format=None):
            if request.method == 'GET':
                print("GET")
                return Response()

            elif request.method == 'POST':
                print("POST")
                print(request.data)
                data = request.data
                prediction, time = rnn_test_data(data)
                if prediction == "null":
                    return Response("预测结果错误，请重试！")
                return Response({
                    "prediction": prediction,
                    "time": time
                })

    class TestOnlyAPI:
        @api_view(['GET', 'POST'])
        def test_model(request, format=None):
            if request.method == 'GET':
                print("GET")
                return Response()

            elif request.method == 'POST':
                print("POST")
                print(request.data)
                data = request.data

                try:
                    response = TextModelBasicInfo.objects.get(user_belong=data["username"], cn_name=data["modelName"], delete_status=0)
                    algorithm = response.algorithm

                except Exception as e:
                    return Response({"模型不存在"})

                test_data = {}
                test_data["username"] = data["username"]
                test_data["modelName"] = data["modelName"]
                test_data["testData"] = data["testData"]
                if algorithm == "KNN":
                    prediction, time = knn_test_data(test_data)
                    if prediction == "null":
                        return Response("预测结果错误，请重试！")
                    return Response({
                        "prediction": prediction,
                        "time": time
                    })

                elif algorithm == "CNN":
                    prediction, time = cnn_test_data(test_data)
                    if prediction == "null":
                        return Response("预测结果错误，请重试！")
                    return Response({
                        "prediction": prediction,
                        "time": time
                    })

                elif algorithm == "RNN":
                    prediction, time = rnn_test_data(test_data)
                    if prediction == "null":
                        return Response("预测结果错误，请重试！")
                    return Response({
                        "prediction": prediction,
                        "time": time
                    })
                else:
                    return Response("模型不可用！")
