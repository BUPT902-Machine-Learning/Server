from rest_framework.response import Response

from cooperation.models import CooperationModels
from numbersDataProcess.interactTrainDataProcess import knn_train_data, cnn_train_data, rnn_train_data
from numbersDataProcess.interactTestDataProcess import knn_test_data
from rest_framework.decorators import api_view

from numbersInteraction.models import NumbersModelBasicInfo, ValueSetData
from users.models import Users


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

    @api_view(['GET', 'POST'])
    def value_set(request, format=None):
        if request.method == 'GET':
            print("GET")
            return Response()

        elif request.method == 'POST':
            print("POST")
            print(request.data)
            raw_data = request.data
            username = raw_data["username"]
            cn_name = raw_data["model_name"]
            value_set_data = raw_data["value_set_data"]
            count = NumbersModelBasicInfo.objects.all().count()
            en_name = "model" + str(count)
            user = Users.objects.get(username=username)
            db_operate = NumbersModelBasicInfo(
                cn_name=cn_name,
                en_name=en_name,
                user_belong=user
            )
            db_operate.save()
            response = NumbersModelBasicInfo.objects.get(en_name=en_name)
            print(value_set_data)
            for item in value_set_data:
                if item["multiSelect"]:
                    separator = ';'
                    multi_select = separator.join(item["multiSelect"])
                else:
                    multi_select = ""

                db_operate = ValueSetData(
                    model_name=response,
                    value=item["value"],
                    type=item["type"],
                    multiSelect=multi_select
                )
                db_operate.save()

            return Response()

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
                    response = NumbersModelBasicInfo.objects.get(user_belong=data["username"], cn_name=data["model_name"])
                    algorithm = response.algorithm

                except Exception as e:
                    return Response({"模型不存在"})

                test_data = dict()
                test_data["username"] = data["username"]
                test_data["model_name"] = data["model_name"]
                test_data["test_data"] = data["test_data"]
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
