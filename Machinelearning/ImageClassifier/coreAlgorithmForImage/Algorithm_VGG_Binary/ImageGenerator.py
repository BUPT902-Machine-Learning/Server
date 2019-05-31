#!/usr/bin/python
# coding:utf8
'''
训练数据生成程序，将每一张输入的训练样本生成进行图像转换后的60张图像样本
'''
from keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img
import os

def training_data_generator(images_info):
    datagen = ImageDataGenerator(rotation_range=40,
                                 width_shift_range=0.2,
                                 height_shift_range=0.2,
                                 shear_range=0.2,
                                 zoom_range=0.2,
                                 horizontal_flip=True,
                                 fill_mode='nearest')
    for image_info in images_info:
        save_path = image_info["save_path"].strip()
        save_path = save_path.rstrip("\\")
        save_train_path = save_path + "/train/" + image_info["label_belong"]
        save_validation_path = save_path + "/validation/" + image_info["label_belong"]
        is_train_exists = os.path.exists(save_train_path)
        is_validation_exists = os.path.exists(save_validation_path)
        if not is_train_exists:
            os.makedirs(save_train_path)
        if not is_validation_exists:
            os.makedirs(save_validation_path)
        for image_name in image_info["images_name"]:
            image_path = image_info["images_path"] + "/" + str(image_name)
            img = load_img(image_path)
            x = img_to_array(img)
            x = x.reshape((1,)+x.shape)
            i = 0
            for batch in datagen.flow(x, batch_size=1,
                                      save_to_dir=save_train_path,
                                      save_prefix=image_info["label_belong"],
                                      save_format='png'):
                i += 1
                if i > 48:
                    break
            for batch in datagen.flow(x, batch_size=1,
                                      save_to_dir=save_validation_path,
                                      save_prefix=image_info["label_belong"],
                                      save_format='png'):
                i += 1
                if i > 60:
                    break