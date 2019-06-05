from rest_framework.decorators import api_view
from rest_framework.response import Response

from classInfo.models import Teacher
from cooperation.models import CooperationData, CooperationImageModels, CooperationImageTrainData, CooperationImageLabelMap

from textDataProcess.dataload import is_py3
from textInteraction.models import TextModelBasicInfo
from modelOperation.interact import utc2local
from users.models import Users

from Machinelearning import settings
import copy
import os
from imageDataProcess import FeatureObtainer, DataAugmentation, FilesDelete
from imageCoreAlgorithm import ModelTesting, ModelTraining
from Machinelearning.settings import BASE_DIR
TRAIN_DATA_ROOT = os.path.join(BASE_DIR, "media").replace('\\', '/')  # media即为图片上传的根路径
AUG_ROOT = os.path.join(BASE_DIR, "aug_images").replace('\\', '/')
MODEL_ROOT = os.path.join(BASE_DIR, "image_model").replace('\\', '/')



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

    # image api
    @api_view(['GET', 'POST'])
    def create_image_model(request, format=None):
        if request.method == 'GET':
            print("GET")
            return Response()

        elif request.method == 'POST':
            print("POST")
            print(request.data)
            try:
                user_belong = Users.objects.get(username=request.data.get('userName'))
                image_model = CooperationImageModels(user_belong=user_belong,
                                                     cn_name=request.data.get('modelName'),
                                                     delete_status=0,
                                                     train_status=0,
                                                     model_type=0)
                count = CooperationImageModels.objects.all().count()
                image_model.en_name = "co_model" + str(count)
                model_name_check = CooperationImageModels.objects.get(user_belong=user_belong,
                                                                      en_name=request.data.get('modelName'))
            except CooperationImageModels.DoesNotExist:
                image_model.save()
                return Response("Create Co-Image Model Success!")
            else:
                return Response("Co-Model Name Check Failed!")

    @api_view(['GET', 'POST'])
    def stu_get_create_image_model(request, format=None):
        if request.method == 'GET':
            print("GET")
            return Response()

        elif request.method == 'POST':
            print("POST")
            print(request.data)
            data = request.data
            create_image_models = []
            try:
                user = Teacher.objects.get(class_no=data["class_no"])
            except Exception as e:
                return Response({"此学生未加入任何班级"})

            db_models = CooperationImageModels.objects.filter(user_belong=user.teacher_name, delete_status=0,
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
                create_image_models.append(model)
            return Response(create_image_models)

    @api_view(['GET', 'POST'])
    def teach_get_create_image_model(request, format=None):
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

            db_models = CooperationImageModels.objects.filter(user_belong=user, delete_status=0,
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
    def get_image_model_data(request, format=None):
        if request.method == 'GET':
            print("GET")
            return Response()

        elif request.method == 'POST':
            print("POST")
            print(request.data)
            data = request.data
            try:
                user_belong = Users.objects.get(username=data["username"])
                model_info = CooperationImageModels.objects.get(user_belong=user_belong, cn_name=data["modelName"],
                                                                delete_status=0, model_type=0)
            except Exception as e:
                return Response({"没有找到此模型"})
            table_data = []
            label_list = model_info.labels.split(",")
            for label in label_list:
                label_data = {}
                image_name = []
                contents = []
                images = CooperationImageTrainData.objects.filter(user_belong=user_belong, model_name=model_info,
                                                                  label=label, delete_status=0)
                for item in images:
                    image_name.append(item.imgName)
                for item in images:
                    contents.append("http://www.localhost.com:8082" + item.content.url)
                label_data["label"] = label
                label_data["image_name"] = image_name
                label_data["contents"] = contents
                table_data.append(label_data)
            return Response({"tableData": table_data})

            return Response(model_datas)

    @api_view(['GET', 'POST'])
    def push_image_data(request, format=None):
        if request.method == 'GET':
            print("GET")
            return Response()

        elif request.method == 'POST':
            print("POST")
            print(request.data)
            data = request.data
            try:
                user_belong = Users.objects.get(username=data["teacher_name"])
                model_exist = CooperationImageTrainData.objects.get(user_belong=user_belong, cn_name=data["model_name"],
                                                                    delete_status=0)

            except Exception as e:
                return Response({"合作模型不存在"})

            try:
                # account = Users.objects.get(username=request.data.get('account'))
                temp = CooperationImageModels.objects.get(user_belong=user_belong, cn_name=data['modelName'])
                img = CooperationImageTrainData(user_belong=user_belong,model_name=temp,
                                                label=request.data.get('label'), delete_status=request.data.get('delete'),
                                                content=request.FILES.get('img'), imgName=request.data.get('imgName'))
                img_check = CooperationImageTrainData.objects.get(model_name=temp,
                                                                  label=request.data.get('label'),
                                                                  imgName=request.data.get('imgName'))
            except CooperationImageTrainData.DoesNotExist:
                img.save()
                return Response("Upload Co-Images Success!")
            if img_check.delete_status == 1:
                img_check.content = img.content
                img_check.delete_status = 0
                img_check.save()
                return Response("Restore Co-Images Success!")
            else:
                return Response("Co-Name Check Failed!")

    @api_view(['GET', 'POST'])
    def pop_image_data(request, format=None):
        if request.method == 'GET':
            print("GET")
            return Response()

        elif request.method == 'POST':
            data = request.data
            print("POST")
            try:
                user = Teacher.objects.get(class_no=data["class_no"])
            except Exception as e:
                return Response({"此学生未加入任何班级"})
            try:
                model_name = CooperationImageModels.objects.get(user_belong=user.teacher_name,
                                                                cn_name=data['modelName'],
                                                                delete_status=0)
                img = CooperationImageTrainData.objects.get(model_name=model_name, label=data['label'],
                                                            imgName=data['imgName'])
                img.delete_status = 1
                img.save()
            except Exception as e:
                return Response("pop image failed")
            return Response("Co-logic delete Success")

    @api_view(['GET', 'POST'])
    def train_image_model(request, format=None):
        if request.method == 'GET':
            print("GET")
            return Response()

        elif request.method == 'POST':
            print("POST")
            data = request.data
            # 提交标签信息以及训练指令
            try:
                # 将标签信息同步至模型基本信息表中
                user_belong = Users.objects.get(username=data['userName'])
                model_info_update = CooperationImageModels.objects.get(user_belong=user_belong,
                                                                       cn_name=data['modelName'])
                label_map = CooperationImageLabelMap.objects.create(model_name=model_info_update)
                labels_list = data['label']
                labels_to_save = ""
                maps_to_save = ""
                map_start = 0
                for label in labels_list:
                    maps_to_save += str(map_start)
                    maps_to_save += ","
                    map_start += 1
                    labels_to_save += label
                    labels_to_save += ","
                labels_to_save = labels_to_save[:-1]
                model_info_update.labels = labels_to_save
                model_info_update.train_status = 1
                model_info_update.save()

                maps_to_save = maps_to_save[:-1]
                label_map.real_labels = labels_to_save
                label_map.train_labels = maps_to_save
                label_map.save()
                # 生成标签对应表，便于训练和测试的统一
                y_dict = {}
                y_dict_map = CooperationImageLabelMap.objects.get(model_name=model_info_update)
                map_list = y_dict_map.train_labels.split(",")
                label_list = y_dict_map.real_labels.split(",")
                for r_label, t_label in zip(label_list, map_list):
                    y_dict.update({r_label: t_label})
                # 生成训练数据信息列表images_info
                images_info = []
                for label in labels_list:
                    image_info = {
                        "model_belong": CooperationImageModels.objects.get(user_belong=user_belong,
                                                                           cn_name=data['modelName']).en_name,
                        "label_belong": label,
                        "base_path": TRAIN_DATA_ROOT,
                        "images_name": []
                    }
                    images_path = os.path.join(TRAIN_DATA_ROOT, image_info["model_belong"], image_info["label_belong"])

                    image_info["images_name"] = os.listdir(images_path)
                    logic_delete_list = []
                    foreign_key = CooperationImageModels.objects.get(en_name=image_info["model_belong"])
                    sql_delete_set = CooperationImageTrainData.objects.filter(model_name=foreign_key,
                                                                              label=image_info["label_belong"],
                                                                              delete_status=1)
                    for item in sql_delete_set:
                        logic_delete_list.append(item.imgName)
                    image_info["images_name"] = list(set(image_info["images_name"]) - set(logic_delete_list))
                    images_info.append(image_info)
                # print(images_info)

                # 数据增强、特征提取和模型训练
                if images_info.__len__() < 2:
                    return Response("The number of labels must be more than 2!")
                elif images_info.__len__() >= 2:
                    augment_images_info = copy.deepcopy(images_info)
                    DataAugmentation.data_augmentation(images_info, augment_images_info)
                    pre_train_model_type = "VGG16"
                    X_train, y_train, X_test, y_test = FeatureObtainer.feature_obtainer(augment_images_info,
                                                                                        pre_train_model_type, y_dict)
                    model_type = "SVM"
                    ModelTraining.model_training(augment_images_info, images_info[0]["model_belong"], model_type,
                                                 X_train, y_train, X_test, y_test)
                    model_info_update.train_status = 2
                    model_info_update.save()
                return Response("Co-Model Training Success!")
            except Exception as e:
                return Response("Co-Model Training Error!")

    @api_view(['GET', 'POST'])
    def if_image_train(request, format=None):
        if request.method == 'GET':
            print("GET")
            return Response()

        elif request.method == 'POST':
            print("POST")
            print(request.data)
            data = request.data

            user_belong = Users.objects.get(username=data['userName'])
            is_train_info = CooperationImageModels.objects.get(user_belong=user_belong,
                                                               cn_name=data['modelName']).train_status
            return Response(is_train_info)

    @api_view(['GET', 'POST'])
    def delete_image_model(request, format=None):
        if request.method == 'GET':
            print("GET")
            return Response()

        elif request.method == 'POST':
            print("POST")
            data = request.data
            try:
                # delete in database
                user_belong = Users.objects.get(username=data['userName'])
                model_name = CooperationImageModels.objects.get(user_belong=user_belong,cn_name=data['modelName'])
                CooperationImageTrainData.objects.filter(user_belong=user_belong, model_name=model_name).delete()
                CooperationImageLabelMap.objects.filter(model_name=model_name).delete()
                CooperationImageModels.objects.filter(user_belong=user_belong, cn_name=data['modelName']).delete()
                # delete the files
                model_file_name = model_name.en_name
                file_path_list = [os.path.join(settings.MEDIA_ROOT, model_file_name).replace('\\', '/'),
                                  os.path.join(AUG_ROOT, model_file_name).replace('\\', '/'),
                                  os.path.join(MODEL_ROOT, model_file_name + "_svm.m").replace('\\', '/')]
                for filePath in file_path_list:
                    FilesDelete.file_delete(filePath)
                return Response("Delete Model Success")
            except Exception as e:
                return Response("Delete Model Failed")
            return Response("Unknown Error of Model Deleting")

    @api_view(['GET', 'POST'])
    def delete_image_label(request, format=None):
        if request.method == 'GET':
            print("GET")
            return Response()

        elif request.method == 'POST':
            print("POST")
            data = request.data
            try:
                # delete in database
                user_belong = Users.objects.get(username=data['userName'])
                model_name = CooperationImageModels.objects.get(user_belong=user_belong,
                                                                cn_name=data['modelName'])
                label_map = CooperationImageLabelMap.objects.get(model_name=model_name)
                CooperationImageTrainData.objects.filter(user_belong=user_belong,
                                                         model_name=model_name,
                                                         label=data['label']).delete()
                label_list = model_name.labels.split(",")
                if label_list.count(data['label']) == 1:
                    label_list.remove(data['label'])
                update_labels = ""
                label_numbers = ""
                numbers = 0
                for label in label_list:
                    label_numbers += str(numbers)
                    update_labels += str(label)
                    label_numbers += ","
                    numbers += 1
                    update_labels += ","
                model_name.labels = update_labels[:-1]
                model_name.save()
                label_map.real_labels = update_labels[:-1]
                label_map.train_labels = label_numbers[:-1]
                label_map.save()
                # delete the files
                model_file_name = model_name.en_name
                # label_file_name = data['label']
                file_path = os.path.join(settings.MEDIA_ROOT, model_file_name, data['label']).replace('\\', '/')
                if os.path.isdir(file_path):
                    delete_list = os.listdir(file_path)
                    while delete_list.__len__() > 0:
                        delete_img = str(file_path) + "/" + str(delete_list[0])
                        os.remove(delete_img)
                        delete_list.remove(delete_list[0])
                    os.rmdir(file_path)
                    return Response("Co-Delete Label Success")
            except Exception as e:
                return Response("Co-Delete Label Failed")
            return Response("Unknown Error")

    @api_view(['GET', 'POST'])
    def test_image_model(request, format=None):
        if request.method == 'GET':
            print("GET")
            return Response()

        elif request.method == 'POST':
            print("POST")
            data = request.data
            # 提交测试图片以及测试指令
            try:
                user_belong = Users.objects.get(username=data['account'])
                model_info_update = CooperationImageModels.objects.get(user_belong=user_belong,
                                                                       cn_name=data['modelName'])
                if model_info_update.train_status == 0:
                    return Response("Co-Model is Untrained!")
                elif model_info_update.train_status == 1:
                    return Response("Co-Model is Training!")
                else:
                    # 生成标签对应表，便于训练和测试的统一
                    y_dict = {}
                    y_dict_map = CooperationImageLabelMap.objects.get(model_name=model_info_update)
                    map_list = y_dict_map.train_labels.split(",")
                    label_list = y_dict_map.real_labels.split(",")
                    for r_label, t_label in zip(label_list, map_list):
                        y_dict.update({r_label: t_label})
                    test_result = ModelTesting.model_testing(data['img'], model_info_update.en_name, y_dict)
                    return Response(test_result)
            except Exception as e:
                return Response("Co-Model Testing Error!")



def native_content(content):
    if not is_py3:
        return content.decode('utf-8')
    else:
        return content