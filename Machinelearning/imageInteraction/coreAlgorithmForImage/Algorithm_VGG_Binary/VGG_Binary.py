#!/usr/bin/python
# coding:utf8
from keras.models import load_model
import numpy as np
from keras.preprocessing import image
from keras.preprocessing.image import load_img
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Dropout, Flatten, Dense
from keras.preprocessing.image import ImageDataGenerator
import cv2
def run_vgg_binary(model_path, train_path, validation_path):
    # 建立模型
    model = Sequential()
    model.add(Conv2D(32, 3, activation='relu', input_shape=(150,150,3)))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(32, 3, activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(64, 3, activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dropout(0.5))    # 冗余过大，建议添加一个dropout
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))
    # 编译
    model.compile(loss='binary_crossentropy',
                  optimizer='rmsprop',
                  metrics=['accuracy'])

    train_datagen = ImageDataGenerator(rescale=1./255,
                                       shear_range=0.2,
                                       zoom_range=0.2,
                                       horizontal_flip=True)
    test_datagen = ImageDataGenerator(rescale=1./255)
    # 从图片中直接产生数据和标签
    train_generator = train_datagen.flow_from_directory(train_path,
                                                        target_size=(150, 150),
                                                        batch_size=32,
                                                        class_mode='binary')

    validation_generator = test_datagen.flow_from_directory(validation_path,
                                                            target_size=(150, 150),
                                                            batch_size=32,
                                                            class_mode='binary')
    model.fit_generator(train_generator,
                        steps_per_epoch=50,
                        epochs=3,
                        validation_data=validation_generator,
                        validation_steps=20)

    # 保存整个模型
    model.save('model.hdf5', model_path)


    # 加载权重
    model = load_model('model.hdf5')

    # 加载图像，预测标签
    img = load_img('C:\\Users\\lenovo\\Desktop\\maibao4.png',target_size=(150, 150))
    img = image.img_to_array(img) / 255.0
    img = np.expand_dims(img, axis=0)

    predictions = model.predict_classes(img)
    print(predictions)

