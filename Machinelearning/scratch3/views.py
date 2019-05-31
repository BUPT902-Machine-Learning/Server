from rest_framework.response import Response

from classInfo.models import Teacher
from textInteraction.models import TextModelBasicInfo
from modelOperation.interact import teach_get_models, stu_get_models, utc2local
from scratch3.interact import get_models, get_labels, test_data_process
from rest_framework.decorators import api_view

from users.models import Users


class API:
    @api_view(['GET', 'POST'])
    def test(request, format=None):
        if request.method == 'GET':
            print("GET")
            return Response()

        elif request.method == 'POST':
            print("POST")
            print(request.data)
            return Response("成功")

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
            create_models = []

            try:
                user = Users.objects.get(username=data["username"])
            except Exception as e:
                return Response({"教师不存在"})

            db_models = TextModelBasicInfo.objects.filter(user_belong=user, delete_status=0,
                                                      model_type=0)
            for item in db_models:
                model = {}
                data_create = utc2local(item.data_create)
                data_update = utc2local(item.data_update)
                model["cn_name"] = item.cn_name
                model["data_create"] = data_create.strftime("%Y-%m-%d %H:%M:%S")
                model["data_update"] = data_update.strftime("%Y-%m-%d %H:%M:%S")
                create_models.append(model)

            return Response({
                "my_models": my_models,
                "stu_models": stu_models,
                "create_models": create_models
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
            create_models = []

            try:
                user = Teacher.objects.get(class_no=data["class_no"])

            except Exception as e:
                return Response({"此学生未加入任何班级"})

            db_models = TextModelBasicInfo.objects.filter(user_belong=user.teacher_name, delete_status=0,
                                                      model_type=0)
            for item in db_models:
                model = {}
                data_create = utc2local(item.data_create)
                data_update = utc2local(item.data_update)
                model["cn_name"] = item.cn_name
                model["teacher"] = user.teacher_name
                model["algorithm"] = item.algorithm
                model["data_create"] = data_create.strftime("%Y-%m-%d %H:%M:%S")
                model["data_update"] = data_update.strftime("%Y-%m-%d %H:%M:%S")
                create_models.append(model)

            return Response({
                "my_models": my_models,
                "teach_models": teach_models,
                "create_models": create_models
            })

    @api_view(['GET', 'POST'])
    def get_labels(request, format=None):
        if request.method == 'GET':
            print("GET")
            return Response()

        elif request.method == 'POST':
            print("POST")
            print(request.data)
            data = request.data
            labels = get_labels(data["username"], data["modelName"])
            return Response(labels)

    @api_view(['GET', 'POST'])
    def use_model(request, format=None):
        if request.method == 'GET':
            print("GET")
            return Response()

        elif request.method == 'POST':
            print("POST")
            print(request.data)
            raw_data = request.data
            prediction, time = test_data_process(raw_data)
            if prediction == "null":
                return Response("null")
            return Response({
                "prediction": prediction,
                "time": time
            })

    @api_view(['GET', 'POST'])
    def stu_get_create_model(request, format=None):
        if request.method == 'GET':
            print("GET")
            return Response()

        elif request.method == 'POST':
            print("POST")
            print(request.data)
            data = request.data
            create_models = []

            try:
                user = Teacher.objects.get(class_no=data["class_no"])

            except Exception as e:
                return Response({"此学生未加入任何班级"})

            db_models = TextModelBasicInfo.objects.filter(user_belong=user.teacher_name, delete_status=0,
                                                      model_type=0)
            for item in db_models:
                model = {}
                data_create = utc2local(item.data_create)
                data_update = utc2local(item.data_update)
                model["cn_name"] = item.cn_name
                model["teacher"] = user.teacher_name
                model["algorithm"] = item.algorithm
                model["data_create"] = data_create.strftime("%Y-%m-%d %H:%M:%S")
                model["data_update"] = data_update.strftime("%Y-%m-%d %H:%M:%S")
                create_models.append(model)

            return Response(create_models)

    @api_view(['GET', 'POST'])
    def teach_get_create_model(request, format=None):
        if request.method == 'GET':
            print("GET")
            return Response()

        elif request.method == 'POST':
            print("POST")
            print(request.data)
            data = request.data
            create_models = []

            try:
                user = Users.objects.get(username=data["teacher_name"])
            except Exception as e:
                return Response({"教师不存在"})

            db_models = TextModelBasicInfo.objects.filter(user_belong=user, delete_status=0,
                                                      model_type=0)
            for item in db_models:
                model = {}
                data_create = utc2local(item.data_create)
                data_update = utc2local(item.data_update)
                model["cn_name"] = item.cn_name
                model["data_create"] = data_create.strftime("%Y-%m-%d %H:%M:%S")
                model["data_update"] = data_update.strftime("%Y-%m-%d %H:%M:%S")
                create_models.append(model)

            return Response(create_models)
