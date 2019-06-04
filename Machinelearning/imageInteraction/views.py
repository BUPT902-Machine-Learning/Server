import copy
from users.models import Users
from imageInteraction.models import ImageModelBasicInfo, TrainData, LabelMap
from Machinelearning import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
import os
from Machinelearning.settings import BASE_DIR
from imageDataProcess import FeatureObtainer, DataAugmentation, FilesDelete
from imageCoreAlgorithm import ModelTesting, ModelTraining
from urllib import parse
TRAIN_DATA_ROOT = os.path.join(BASE_DIR, "media").replace('\\', '/')  # media即为图片上传的根路径
AUG_ROOT = os.path.join(BASE_DIR, "aug_images").replace('\\', '/')
MODEL_ROOT = os.path.join(BASE_DIR, "image_model").replace('\\', '/')


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
                img_check.content = img.content
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
                modelName = ImageModelBasicInfo.objects.get(cn_name=request.data.get('modelName'))
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
                user_belong = Users.objects.get(username=request.data.get('userName'))
                model_name = ImageModelBasicInfo.objects.get(user_belong=user_belong, cn_name=request.data.get('modelName'))
                label_map = LabelMap.objects.get(model_name=model_name)
                TrainData.objects.filter(user_belong=user_belong,
                                         model_name=model_name, label=request.data.get('label')).delete()
                label_list = model_name.labels.split(",")
                if label_list.count(request.data.get('label')) == 1:
                    label_list.remove(request.data.get('label'))
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
                label_file_name = request.data.get('label')
                file_path = os.path.join(settings.MEDIA_ROOT, model_file_name, label_file_name).replace('\\', '/')
                if os.path.isdir(file_path):
                    delete_list = os.listdir(file_path)
                    while delete_list.__len__() > 0:
                        delete_img = str(file_path) + "/" + str(delete_list[0])
                        os.remove(delete_img)
                        delete_list.remove(delete_list[0])
                    os.rmdir(file_path)
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
                user_belong = Users.objects.get(username=request.data.get('userName'))
                model_name = ImageModelBasicInfo.objects.get(user_belong=user_belong, cn_name=request.data.get('modelName'))
                TrainData.objects.filter(user_belong=user_belong, model_name=model_name).delete()
                LabelMap.objects.filter(model_name=model_name).delete()
                ImageModelBasicInfo.objects.filter(user_belong=user_belong,cn_name=request.data.get('modelName')).delete()
                # print("test")
                # delete the files
                model_file_name = model_name.en_name
                file_path_list = [os.path.join(settings.MEDIA_ROOT, model_file_name).replace('\\', '/'),
                                  os.path.join(AUG_ROOT, model_file_name).replace('\\', '/'),
                                  os.path.join(MODEL_ROOT, model_file_name+"_svm.m").replace('\\', '/')]
                for filePath in file_path_list:
                    FilesDelete.file_delete(filePath)
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
                label_map = LabelMap.objects.create(model_name=model_info_update)
                labels_list = request.data.get('label')
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
                model_info_update.public_status = request.data.get('publicStatus')
                model_info_update.save()

                maps_to_save = maps_to_save[:-1]
                label_map.real_labels = labels_to_save
                label_map.train_labels = maps_to_save
                label_map.save()
                # 生成标签对应表，便于训练和测试的统一
                y_dict = {}
                y_dict_map = LabelMap.objects.get(model_name=model_info_update)
                map_list = y_dict_map.train_labels.split(",")
                label_list = y_dict_map.real_labels.split(",")
                for r_label, t_label in zip(label_list, map_list):
                    y_dict.update({r_label: t_label})
                # 生成训练数据信息列表images_info
                images_info = []
                for label in labels_list:
                    image_info = {
                        "model_belong": ImageModelBasicInfo.objects.get(user_belong=user_belong, cn_name=request.data.
                                                                        get('modelName')).en_name,
                        "label_belong": label,
                        "base_path": TRAIN_DATA_ROOT,
                        "images_name": []
                    }
                    images_path = os.path.join(TRAIN_DATA_ROOT, image_info["model_belong"], image_info["label_belong"])

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
                user_belong = Users.objects.get(username=request.data.get('account'))
                model_info_update = ImageModelBasicInfo.objects.get(user_belong=user_belong,
                                                                    cn_name=request.data.get('modelName'))
                if model_info_update.train_status == 0:
                    return Response("Model is Untrained!")
                elif model_info_update.train_status == 1:
                    return Response("Model is Training!")
                else:
                    # 生成标签对应表，便于训练和测试的统一
                    y_dict = {}
                    y_dict_map = LabelMap.objects.get(model_name=model_info_update)
                    map_list = y_dict_map.train_labels.split(",")
                    label_list = y_dict_map.real_labels.split(",")
                    for r_label, t_label in zip(label_list, map_list):
                        y_dict.update({r_label: t_label})
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
            train_status = ImageModelBasicInfo.objects.get(user_belong=user_belong,
                                                           cn_name=request.data.get('modelName')).train_status
            return Response(train_status)

    @api_view(['GET', 'POST'])
    def edit_img_model(request, format=None):
        if request.method == 'GET':
            print("GET")
            return Response()

        elif request.method == 'POST':
            print("POST")
            print(request.data)
            user_belong = Users.objects.get(username=request.data.get('userName'))
            model_info = ImageModelBasicInfo.objects.get(user_belong=user_belong, cn_name=request.data.get('modelName'))
            table_data = []
            label_list = model_info.labels.split(",")
            for label in label_list:
                label_data = {}
                image_name = []
                contents = []
                images = TrainData.objects.filter(user_belong=user_belong, model_name=model_info, label=label,
                                                  delete_status=0)
                for item in images:
                    image_name.append(item.imgName)
                for item in images:
                    # str_url = parse.unquote(item.content.url)
                    contents.append("http://www.localhost.com:8082" + item.content.url)
                label_data["label"] = label
                label_data["image_name"] = image_name
                label_data["contents"] = contents
                table_data.append(label_data)
            return Response({"tableData": table_data})

    @api_view(['GET', 'POST'])
    def re_train_img_model(request, format=None):
        if request.method == 'GET':
            print("GET")
            return Response()

        elif request.method == 'POST':
            print("POST")
            # 提交标签信息以及训练指令
            try:
                if request.data.get('isChange') == 0:
                    return Response("model info is same to old version")
                else:
                    # 删除预先保留的数据增强以及模型信息
                    print(request.data)
                    user_belong = Users.objects.get(username=request.data.get('userName'))
                    model_name = ImageModelBasicInfo.objects.get(user_belong=user_belong,
                                                                 cn_name=request.data.get('modelName'))
                    model_file_name = model_name.en_name
                    file_path_list = [os.path.join(AUG_ROOT, model_file_name).replace('\\', '/'),
                                      os.path.join(MODEL_ROOT, model_file_name + "_svm.m").replace('\\', '/')]
                    for filePath in file_path_list:
                        FilesDelete.file_delete(filePath)
                    # 将标签信息同步至模型基本信息表中
                    user_belong = Users.objects.get(username=request.data.get('userName'))
                    model_info_update = ImageModelBasicInfo.objects.get(user_belong=user_belong,
                                                                        cn_name=request.data.get('modelName'))
                    label_map = LabelMap.objects.get(model_name=model_info_update)
                    labels_list = request.data.get('label')
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
                    model_info_update.public_status = request.data.get('publicStatus')
                    model_info_update.save()

                    maps_to_save = maps_to_save[:-1]
                    label_map.real_labels = labels_to_save
                    label_map.train_labels = maps_to_save
                    label_map.save()
                    # 生成标签对应表，便于训练和测试的统一
                    y_dict = {}
                    y_dict_map = LabelMap.objects.get(model_name=model_info_update)
                    map_list = y_dict_map.train_labels.split(",")
                    label_list = y_dict_map.real_labels.split(",")
                    for r_label, t_label in zip(label_list, map_list):
                        y_dict.update({r_label: t_label})
                    # 生成训练数据信息列表images_info
                    images_info = []
                    for label in labels_list:
                        image_info = {
                            "model_belong": ImageModelBasicInfo.objects.get(user_belong=user_belong, cn_name=request.data.
                                                                            get('modelName')).en_name,
                            "label_belong": label,
                            "base_path": TRAIN_DATA_ROOT,
                            "images_name": []
                        }
                        images_path = os.path.join(TRAIN_DATA_ROOT, image_info["model_belong"], image_info["label_belong"])

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
                        X_train, y_train, X_test, y_test = FeatureObtainer.feature_obtainer(augment_images_info,
                                                                                            pre_train_model_type, y_dict)
                        model_type = "SVM"
                        ModelTraining.model_training(augment_images_info, images_info[0]["model_belong"], model_type,
                                                     X_train, y_train, X_test, y_test)
                        model_info_update.train_status = 2
                        model_info_update.save()
                    return Response("Model Re-Training Success!")
            except Exception as e:
                return Response("Model Re-Training Error!")











