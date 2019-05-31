import copy
from users.models import Users
from imageInteraction.models import ImageModelBasicInfo, TrainData
from Machinelearning import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
import os
from Machinelearning.settings import BASE_DIR
from imageDataProcess import FeatureObtainer, DataAugmentation
from imageCoreAlgorithm import ModelTesting, ModelTraining
from modelOperation.interact import utc2local
from users.models import Student
from classInfo.models import Teacher
TRAINDATA_ROOT = os.path.join(BASE_DIR, "media").replace('\\', '/')  # media即为图片上传的根路径


class ImageClassifierAPI:
    @api_view(['GET', 'POST'])
    def teach_get_co_model(request, format=None):
        if request.method == 'GET':
            print("GET")
            return Response()
        elif request.method == 'POST':
            print("POST")
            print(request.data)
            return Response("todo")

    @api_view(['GET', 'POST'])
    def stu_get_co_model(request, format=None):
        if request.method == 'GET':
            print("GET")
            return Response()
        elif request.method == 'POST':
            print("POST")
            print(request.data)
            return Response("todo")

    # @api_view(['GET', 'POST'])
    # def teach_get_model(request, format=None):
    #     if request.method == 'GET':
    #         print("GET")
    #         return Response()
    #     elif request.method == 'POST':
    #         print("POST")
    #         print(request.data)
    #         data = request.data
    #         my_models = []
    #         stu_models = []
    #         db_models = ImageModelBasicInfo.objects.filter(user_belong=data["username"], delete_status=0, model_type=2)
    #         for item in db_models:
    #             model = {}
    #             data_create = utc2local(item.data_create)
    #             data_update = utc2local(item.data_update)
    #             model["cn_name"] = item.cn_name
    #             model["algorithm"] = item.algorithm
    #             model["data_create"] = data_create.strftime("%Y-%m-%d %H:%M:%S")
    #             model["data_update"] = data_update.strftime("%Y-%m-%d %H:%M:%S")
    #             my_models.append(model)
    #
    #         db_student = Student.objects.filter(class_no=data["class_no"])
    #         for item in db_student:
    #             db_models = ImageModelBasicInfo.objects.filter(user_belong=item.student_name, delete_status=0,
    #                                                            public_status=1)
    #             stu_model = []
    #             for item2 in db_models:
    #                 model = {}
    #                 data_create = utc2local(item2.data_create)
    #                 data_update = utc2local(item2.data_update)
    #                 model["user_name"] = item.student_name
    #                 model["en_name"] = item2.en_name
    #                 model["algorithm"] = item2.algorithm
    #                 model["data_create"] = data_create.strftime("%Y-%m-%d %H:%M:%S")
    #                 model["data_update"] = data_update.strftime("%Y-%m-%d %H:%M:%S")
    #                 stu_model.append(model)
    #
    #             stu_models.append(stu_model)
    #         return Response({
    #             "my_models": my_models,
    #             "stu_models": stu_models
    #         })
    #
    # @api_view(['GET', 'POST'])
    # def stu_get_model(request, format=None):
    #     if request.method == 'GET':
    #         print("GET")
    #         return Response()
    #
    #     elif request.method == 'POST':
    #         print("POST")
    #         print(request.data)
    #         data = request.data
    #         my_models = []
    #         tech_models = []
    #         db_models = ImageModelBasicInfo.objects.filter(user_belong=data["username"], delete_status=0)
    #         for item in db_models:
    #             model = {}
    #             data_create = utc2local(item.data_create)
    #             data_update = utc2local(item.data_update)
    #             model["cn_name"] = item.cn_name
    #             model["algorithm"] = item.algorithm
    #             model["data_create"] = data_create.strftime("%Y-%m-%d %H:%M:%S")
    #             model["data_update"] = data_update.strftime("%Y-%m-%d %H:%M:%S")
    #             my_models.append(model)
    #         try:
    #             db_teacher = Teacher.objects.get(class_no=data["class_no"])
    #             db_models = ImageModelBasicInfo.objects.filter(user_belong=db_teacher.teacher_name, delete_status=0,
    #                                                            public_status=1, model_type=2)
    #
    #         except Exception as e:
    #             return my_models, False
    #
    #         for item in db_models:
    #             model = {}
    #             data_create = utc2local(item.data_create)
    #             data_update = utc2local(item.data_update)
    #             model["tech_name"] = db_teacher.teacher_name
    #             model["cn_name"] = item.cn_name
    #             model["algorithm"] = item.algorithm
    #             model["data_create"] = data_create.strftime("%Y-%m-%d %H:%M:%S")
    #             model["data_update"] = data_update.strftime("%Y-%m-%d %H:%M:%S")
    #             tech_models.append(model)
    #
    #         return Response({
    #             "my_models": my_models,
    #             "tech_models": tech_models
    #         })

    @api_view(['GET', 'POST'])
    def save_data(request, format=None):
        if request.method == 'GET':
            print("GET")
            return Response()

        elif request.method == 'POST':
            print("POST")
            try:
                account = Users.objects.get(username=request.data.get('account'))
                temp = ImageModelBasicInfo.objects.get(user_belong=account, cn_name=request.data.get('modelName'))
                img = TrainData(user_belong=account,
                                model_name=temp,
                                label=request.data.get('label'),
                                delete_status=request.data.get('delete'),
                                content=request.FILES.get('img'),
                                imgName=request.data.get('imgName'))
                img_check = TrainData.objects.get(model_name=temp,
                                                  label=request.data.get('label'),
                                                  imgName=request.data.get('imgName'))
            except TrainData.DoesNotExist:
                img.save()
                return Response("Upload Images Success!")
            if img_check.delete_status == 1:
                img_check.delete_status = 0
                img_check.save()
                return Response("Restore Images Success!")
            else:
                return Response("Name Check Failed!")

    @api_view(['GET', 'POST'])
    def delete_data(request, format=None):
        if request.method == 'GET':
            print("GET")
            return Response()

        elif request.method == 'POST':
            print("POST")
            try:
                modelName = ImageModelBasicInfo.objects.get(en_name=request.data.get('modelName'))
                img = TrainData.objects.get(model_name=modelName,
                                            label=request.data.get('label'),
                                            imgName=request.data.get('imgName'))
                img.delete_status = 1
                img.save()
            except Exception as e:
                return Response("failed")
            return Response("logic delete Success")

    @api_view(['GET', 'POST'])
    def delete_label(request, format=None):
        if request.method == 'GET':
            print("GET")
            return Response()

        elif request.method == 'POST':
            print("POST")
            try:
                # delete in database
                modelName = ImageModelBasicInfo.objects.get(en_name=request.data.get('modelName'))
                TrainData.objects.filter(model_name=modelName,label=request.data.get('label')).delete()
                # delete the file
                modelFileName = request.data.get('modelName')
                labelFileName = request.data.get('label')
                filePath = os.path.join(settings.MEDIA_ROOT, modelFileName, labelFileName).replace('\\', '/')
                if os.path.isdir(filePath):
                    deleteList = os.listdir(filePath)
                    while deleteList.__len__() > 0:
                        deleteImg = str(filePath) + "/" + str(deleteList[0])
                        os.remove(deleteImg)
                        deleteList.remove(deleteList[0])
                    os.rmdir(filePath)
                    return Response("Delete Label Success")
            except Exception as e:
                return Response("Delete Label Failed")
            return Response("Unknown Error")

    @api_view(['GET', 'POST'])
    def create_model(request, format=None):
        if request.method == 'GET':
            print("GET")
            return Response()

        elif request.method == 'POST':
            print("POST")
            try:
                user_belong = Users.objects.get(username=request.data.get('userName'))
                imgModel = ImageModelBasicInfo(user_belong=user_belong,
                                               cn_name=request.data.get('modelName'),
                                               delete_status=0,
                                               public_status=1,
                                               train_status=0,
                                               model_type=1)
                count = ImageModelBasicInfo.objects.all().count()
                imgModel.en_name = "model" + str(count)
                modelNameCheck = ImageModelBasicInfo.objects.get(user_belong=user_belong,
                                                                 en_name=request.data.get('modelName'))
            except ImageModelBasicInfo.DoesNotExist:
                imgModel.save()
                return Response("Create Image Model Success!")
            else:
                return Response("Model Name Check Failed!")

    @api_view(['GET', 'POST'])
    def delete_model(request, format=None):
        if request.method == 'GET':
            print("GET")
            return Response()

        elif request.method == 'POST':
            print("POST")
            try:
                # delete in database
                modelName = ImageModelBasicInfo.objects.get(en_name=request.data.get('modelName'))
                TrainData.objects.filter(model_name=modelName).delete()
                User_belong = Users.objects.get(username=request.data.get('userName'))
                ImageModelBasicInfo.objects.filter(user_belong=User_belong).delete()
                # delete the file
                modelFileName = request.data.get('modelName')
                filePath = os.path.join(settings.MEDIA_ROOT, modelFileName).replace('\\', '/')
                if os.path.isdir(filePath):
                    os.rmdir(filePath)
                    return Response("Delete Model Success")
            except Exception as e:
                return Response("Delete Model Failed")
            return Response("Unknown Error of Model Deleting")

    @api_view(['GET', 'POST'])
    def train_model(request, format=None):
        if request.method == 'GET':
            print("GET")
            return Response()

        elif request.method == 'POST':
            print("POST")
            # 提交标签信息以及训练指令
            try:
                # 将标签信息同步至模型基本信息表中
                user_belong = Users.objects.get(username=request.data.get('userName'))
                model_info_update = ImageModelBasicInfo.objects.get(user_belong=user_belong,
                                                                    cn_name=request.data.get('modelName'))

                labels_list = request.data.get('label')
                labels_to_save = ""
                for label in labels_list:
                    labels_to_save += label
                    labels_to_save += ","
                labels_to_save = labels_to_save[:-1]
                model_info_update.labels = labels_to_save
                model_info_update.train_status = 1
                model_info_update.public_status = request.data.get('publicStatus')
                model_info_update.save()
                # 生成标签对应表，便于训练和测试的统一
                y_dict = {}
                label_id = 0
                label_list = model_info_update.labels.split(",")
                for label in label_list:
                    y_dict.update({label: label_id})
                    label_id += 1
                # 生成训练数据信息列表images_info
                images_info = []
                for label in labels_list:
                    image_info = {
                        "model_belong": ImageModelBasicInfo.objects.get(user_belong=user_belong, cn_name=request.data.
                                                                        get('modelName')).en_name,
                        "label_belong": label,
                        "base_path": TRAINDATA_ROOT,
                        "images_name": []
                    }
                    images_path = os.path.join(TRAINDATA_ROOT, image_info["model_belong"], image_info["label_belong"])

                    image_info["images_name"] = os.listdir(images_path)
                    logic_delete_list = []
                    foreign_key = ImageModelBasicInfo.objects.get(en_name=image_info["model_belong"])
                    sql_delete_set = TrainData.objects.filter(model_name=foreign_key,
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
                    X_train, y_train, X_test, y_test = FeatureObtainer.feature_obtainer(augment_images_info, pre_train_model_type, y_dict)
                    model_type = "SVM"
                    ModelTraining.model_training(augment_images_info, images_info[0]["model_belong"], model_type, X_train, y_train, X_test, y_test)
                    model_info_update.train_status = 2
                    model_info_update.save()
                return Response("Model Training Success!")
            except Exception as e:
                return Response("Model Training Error!")

    @api_view(['GET', 'POST'])
    def test_model(request, format=None):
        if request.method == 'GET':
            print("GET")
            return Response()

        elif request.method == 'POST':
            print("POST")
            # 提交测试图片以及测试指令
            try:
                y_dict = {}
                label_id = 0
                user_belong = Users.objects.get(username=request.data.get('account'))
                model_info_update = ImageModelBasicInfo.objects.get(user_belong=user_belong,
                                                                    cn_name=request.data.get('modelName'))
                if model_info_update.train_status == 0:
                    return Response("Model is Untrained!")
                elif model_info_update.train_status == 1:
                    return Response("Model is Training!")
                else:
                    label_list = model_info_update.labels.split(",")
                    for label in label_list:
                        y_dict.update({label: label_id})
                        label_id += 1
                    test_result = ModelTesting.model_testing(request.FILES.get('img'), model_info_update.en_name, y_dict)
                    return Response(test_result)
            except Exception as e:
                return Response("Model Testing Error!")

    @api_view(['GET', 'POST'])
    def train_status_check(request, format=None):
        if request.method == 'GET':
            print("GET")
            return Response()

        elif request.method == 'POST':
            print("POST")
            user_belong = Users.objects.get(username=request.data.get('userName'))
            train_status = ImageModelBasicInfo.objects.get(user_belong=user_belong, cn_name=request.data.get('modelName')).train_status
            return Response(train_status)











