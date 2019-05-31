import os
from keras.applications.vgg16 import VGG16
from keras.applications.vgg19 import VGG19
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input
from keras.models import Model
import numpy as np
from Machinelearning.settings import BASE_DIR


def feature_obtainer(augment_images_info, pre_train_model_type, y_dict):
    if pre_train_model_type == "VGG16":
        base_model = VGG16(weights='imagenet', include_top=True)  # 加载VGG16模型及参数
    else:
        base_model = VGG19(weights='imagenet', include_top=True)  # 加载VGG19模型及参数
    model = Model(inputs=base_model.input, outputs=base_model.get_layer('predictions').output)
    print("Model", pre_train_model_type, " has been onload !")
    X_list_train = []
    y_train = []
    X_list_test = []
    y_test = []
    for augment_image_info in augment_images_info:
        i = 0
        for item in augment_image_info["images_name"]:
            file_path = os.path.join(BASE_DIR, "aug_images",
                                     augment_image_info["model_belong"],
                                     augment_image_info["label_belong"],
                                     item)
            img = image.load_img(file_path, target_size=(224, 224))
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = preprocess_input(x)
            fc = model.predict(x)  # 获取VGG19全连接层特征
            if i <= 0.8 * len(augment_image_info["images_name"]):
                X_list_train.append(fc.tolist()[0])
                y_train.append(y_dict[augment_image_info["label_belong"]])
            else:
                X_list_test.append(fc.tolist()[0])
                y_test.append(y_dict[augment_image_info["label_belong"]])
            i += 1
    X_train = np.array(X_list_train)
    X_test = np.array(X_list_test)
    # print(type(X_train), X_train.shape, type(X_train[0]), X_train[0].shape)
    print("Features has been obtained !")
    return X_train, y_train, X_test, y_test