from rest_framework.response import Response
from rest_framework.decorators import api_view

from imageInteraction.models import ImageModelBasicInfo
from numbersInteraction.models import NumbersModelBasicInfo
from textInteraction.models import TextModelBasicInfo
from .interact import stu_get_models, delete_models, text_edit_model, numbers_edit_model, image_edit_model, \
    teach_get_models, test_model_get_value


class API:
    # @api_view(['GET', 'POST'])
    # def get_models(request, format=None):
    #     if request.method == 'GET':
    #         print("GET")
    #         return Response()
    #
    #     elif request.method == 'POST':
    #         print("POST")
    #         print(request.data)
    #         data = request.data
    #         models = get_models(data["username"])
    #         return Response(models)

    @api_view(['GET', 'POST'])
    def named_check(request, format=None):
        if request.method == 'GET':
            print("GET")
            return Response()

        elif request.method == 'POST':
            print("POST")
            print(request.data)
            data = request.data
            train_data_type = data["train_data_type"]
            if train_data_type == "text":
                response = TextModelBasicInfo.objects.filter(user_belong=data["username"], cn_name=data["model_name"], delete_status=0)

            elif train_data_type == "numbers":
                response = NumbersModelBasicInfo.objects.filter(user_belong=data["username"],
                                                                cn_name=data["model_name"], delete_status=0)
            else:
                response = ImageModelBasicInfo.objects.filter(user_belong=data["username"], cn_name=data["model_name"], delete_status=0)

            if response:
                return Response({"模型名已存在"})

            return Response({"模型名未存在"})

    @api_view(['GET', 'POST'])
    def delete_model(request, format=None):
        if request.method == 'GET':
            print("GET")
            return Response()

        elif request.method == 'POST':
            print("POST")
            print(request.data)
            data = request.data
            ret_msg = delete_models(data["username"], data["modelName"], data["data_type"])
            return Response(ret_msg)

    @api_view(['GET', 'POST'])
    def text_edit_model(request, format=None):
        if request.method == 'GET':
            print("GET")
            return Response()

        elif request.method == 'POST':
            print("POST")
            print(request.data)
            data = request.data
            train_data, params, algorithm, is_public = text_edit_model(data["username"], data["modelName"])
            return Response({
                "trainData": train_data,
                "params": params,
                "algorithm": algorithm,
                "isPublic": is_public
            })

    @api_view(['GET', 'POST'])
    def numbers_edit_model(request, format=None):
        if request.method == 'GET':
            print("GET")
            return Response()

        elif request.method == 'POST':
            print("POST")
            print(request.data)
            data = request.data
            train_data, value_data, params, algorithm, is_public = numbers_edit_model(data["username"], data["modelName"])
            return Response({
                "trainData": train_data,
                "valueData": value_data,
                "params": params,
                "algorithm": algorithm,
                "isPublic": is_public
            })

    @api_view(['GET', 'POST'])
    def test_model_get_value(request, format=None):
        if request.method == 'GET':
            print("GET")
            return Response()

        elif request.method == 'POST':
            print("POST")
            print(request.data)
            data = request.data
            value_data = test_model_get_value(data["username"], data["modelName"])
            return Response({
                "valueData": value_data,
            })

    @api_view(['GET', 'POST'])
    def image_edit_model(request, format=None):
        if request.method == 'GET':
            print("GET")
            return Response()

        elif request.method == 'POST':
            print("POST")
            print(request.data)
            data = request.data
            train_data, params, algorithm, is_public = image_edit_model(data["username"], data["modelName"])
            return Response({
                "trainData": train_data,
                "params": params,
                "algorithm": algorithm,
                "isPublic": is_public
            })

    @api_view(['GET', 'POST'])
    def teach_get_models(request, format=None):
        if request.method == 'GET':
            print("GET")
            return Response()

        elif request.method == 'POST':
            print("POST")
            print(request.data)
            data = request.data
            my_models, stu_models = teach_get_models(data["username"], data["class_no"])
            return Response({
                "my_models": my_models,
                "stu_models": stu_models
            })

    @api_view(['GET', 'POST'])
    def stu_get_models(request, format=None):
        if request.method == 'GET':
            print("GET")
            return Response()

        elif request.method == 'POST':
            print("POST")
            print(request.data)
            data = request.data
            my_models, teach_models = stu_get_models(data["username"], data["class_no"])
            return Response({
                "my_models": my_models,
                "teach_models": teach_models
            })
