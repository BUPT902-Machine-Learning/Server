import os
from keras.applications.vgg16 import VGG16
from keras.applications.vgg19 import VGG19
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input
from keras.models import Model
import numpy as np
from sklearn.externals import joblib

from Machinelearning.settings import BASE_DIR


def model_testing(test_image, model_id, y_dict):
    # 完成对图片的特征提取
    base_model = VGG16(weights='imagenet', include_top=True)  # 加载VGG16模型及参数
    model = Model(inputs=base_model.input, outputs=base_model.get_layer('predictions').output)
    x = image.load_img(test_image, target_size=(224, 224))
    x = image.img_to_array(x)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    fc = model.predict(x)

    # 完成模型的加载和对目标图片的预测
    file_path = os.path.join(BASE_DIR, "image_model", model_id+"_svm.m")
    clf = joblib.load(file_path)
    prediction = clf.predict(fc)
    print(prediction, y_dict)
    for item in y_dict:
        if y_dict[item] == prediction[0]:
            print(item)
            return item
    return "error"
