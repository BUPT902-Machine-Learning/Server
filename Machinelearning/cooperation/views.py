from rest_framework.decorators import api_view
from rest_framework.response import Response

from classInfo.models import Teacher
from cooperation.models import CooperationData

from textDataProcess.dataload import is_py3
from textInteraction.models import TextModelBasicInfo
from modelOperation.interact import utc2local
from users.models import Users


def get_train_data(train_data):
    labels, contents, label_content = [], [], []

    for item in train_data:
        try:
            label = item["label"]
            labels.append(label)
            for content in item["contents"]:
                contents.append(content)
                label_content.append(label)

        except:
            pass

    return labels, contents, label_content


def encapsulation_data(labels, label_content, contents):
    print(labels)
    print(label_content)
    print(contents)
    model_datas = []
    for item in labels:
        model_data = {}
        model_data["label"] = item
        model_data["content"] = []
        model_datas.append(model_data)

    i = 0
    for item in label_content:
        try:
            j = labels.index(item)
            if contents[i] not in model_datas[j]["content"]:
                model_datas[j]["content"].append(contents[i])

        except Exception as e:
            pass

        i = i + 1

    return model_datas


class API:
    @api_view(['GET', 'POST'])
    def create_model(request, format=None):
        if request.method == 'GET':
            print("GET")
            return Response()

        elif request.method == 'POST':
            print("POST")
            print(request.data)
            raw_data = request.data
            count = TextModelBasicInfo.objects.all().count()
            en_name = "model" + str(count)
            cn_name = raw_data["modelName"]
            username = raw_data["username"]

            try:
                user = Users.objects.get(username=username)

            except Exception as e:
                return Response({
                    "教师不存在"
                })

            train_data = raw_data["trainData"]
            train_labels, train_contents, label_content = get_train_data(train_data)
            separator = ';'
            db_labels = separator.join(train_labels)
            db_label_content = separator.join(label_content)
            db_contents = separator.join(train_contents)
            print(db_labels)
            print(db_contents)
            db_operate = TextModelBasicInfo(
                cn_name=cn_name,
                en_name=en_name,
                user_belong=user,
                model_type=0,
                labels=db_labels,
                label_content=db_label_content,
                contents=db_contents
            )
            db_operate.save()

            return Response({
                "添加成功"
            })

    @api_view(['GET', 'POST'])
    def delete_model(request, format=None):
        if request.method == 'GET':
            print("GET")
            return Response()

        elif request.method == 'POST':
            print("POST")
            print(request.data)
            data = request.data

            try:
                TextModelBasicInfo.objects.filter(user_belong=data["username"], cn_name=data["modelName"])\
                    .update(delete_status=1)

            except Exception as e:
                return Response({"delete_error"})

            return Response({"delete_confirm"})

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

    @api_view(['GET', 'POST'])
    def get_model_data(request, format=None):
        if request.method == 'GET':
            print("GET")
            return Response()

        elif request.method == 'POST':
            print("POST")
            print(request.data)
            data = request.data

            try:
                user = Users.objects.get(username=data["username"])
                db_model_data = TextModelBasicInfo.objects.get(user_belong=user, cn_name=data["modelName"],
                                                           delete_status=0, model_type=0)
            except Exception as e:
                return Response({"没有找到此模型"})

            db_labels = db_model_data.labels
            db_label_content = db_model_data.label_content
            db_contents = db_model_data.contents
            labels = db_labels.split(";")
            label_content = db_label_content.split(";")
            contents = db_contents.split(";")
            model_datas = encapsulation_data(labels, label_content, contents)

            return Response(model_datas)

    @api_view(['GET', 'POST'])
    def push_data(request, format=None):
        if request.method == 'GET':
            print("GET")
            return Response()

        elif request.method == 'POST':
            print("POST")
            print(request.data)
            data = request.data

            try:
                user = Users.objects.get(username=data["teacher_name"])
                en_name = TextModelBasicInfo.objects.get(user_belong=user, cn_name=data["model_name"], delete_status=0)

            except Exception as e:
                return Response({"模型不存在"})

            train_labels, train_contents, label_content = get_train_data(data["train_data"])
            separator = ';'
            db_label_content = separator.join(label_content)
            db_contents = separator.join(train_contents)
            db_operate = CooperationData(
                en_name=en_name,
                student_name=data["student_name"],
                label_content=db_label_content,
                contents=db_contents,
            )
            db_operate.save()

            return Response()

    @api_view(['GET', 'POST'])
    def train_model(request, format=None):
        if request.method == 'GET':
            print("GET")
            return Response()

        elif request.method == 'POST':
            print("POST")
            print(request.data)
            data = request.data

            try:
                en_name = TextModelBasicInfo.objects.get(user_belong=data["teacher_name"], cn_name=data["model_name"],
                                                     delete_status=0)

            except Exception as e:
                return Response({"模型不存在"})

            str_label_content = en_name.label_content
            str_contents = en_name.contents
            student_push_data = CooperationData.objects.filter(en_name=en_name)

            if str_label_content != "":
                for item in student_push_data:
                    str_label_content = str_label_content + ";" + item.label_content
                    str_contents = str_contents + ";" + item.contents
            else:
                student_data = list(student_push_data)
                if student_data:
                    student = student_data.pop(0)
                    str_label_content = student.label_content
                    str_contents = student.contents
                    for item in student_push_data:
                        str_label_content = str_label_content + ";" + item.label_content
                        str_contents = str_contents + ";" + item.contents

            labels = en_name.labels.split(";")
            label_content = str_label_content.split(";")
            contents = str_contents.split(";")
            model_datas = encapsulation_data(labels, label_content, contents)

            return Response({
                "algorithm": en_name.algorithm,
                "model_datas": model_datas
            })

    @api_view(['GET', 'POST'])
    def if_train(request, format=None):
        if request.method == 'GET':
            print("GET")
            return Response()

        elif request.method == 'POST':
            print("POST")
            print(request.data)
            data = request.data

            response = TextModelBasicInfo.objects.filter(user_belong=data["username"], cn_name=data["modelName"])
            print("algop")
            print(response[0].algorithm)

            if response[0].algorithm:
                return Response({"模型已训练"})

            return Response({"模型未训练"})


def native_content(content):
    if not is_py3:
        return content.decode('utf-8')
    else:
        return content