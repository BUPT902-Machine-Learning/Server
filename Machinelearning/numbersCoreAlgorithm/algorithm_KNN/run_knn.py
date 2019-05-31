import jieba
import pandas as pd
import random
import numpy as np
import time
from datetime import timedelta
import os
import itertools
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.externals import joblib
from textDataProcess.dataload import move_stop_word


def get_time_dif(start_time):
    """获取已使用时间"""
    end_time = time.time()
    time_dif = end_time - start_time
    return timedelta(seconds=int(round(time_dif)))


def tokenizer(s):
    words = []
    cut = jieba.cut(s)
    for word in cut:
        if_stop = move_stop_word(word)
        if if_stop:
            words.append(word)
    return words


def int2bin(n, count=24):
    """returns the binary of integer n, using count number of digits"""
    return "".join([str((n >> y) & 1) for y in range(count-1, -1, -1)])


def evaluate(y_preds, y_labels):
    num = 0
    count = 0
    for pred, label in zip(y_preds, y_labels):
        count = count + 1
        if pred == label:
            num = num + 1

    return float(num/count)


def train(contents, labels, save_dir, k):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    model_path = os.path.join(save_dir, 'trainModel.pkl')
    tf_idf_feature_path = os.path.join(save_dir, 'tfIdfFeature.pkl')

    start_time = time.time()
    form = pd.DataFrame(columns=['contents', 'labels'])
    for content, label in zip(contents, labels):
        form.loc[len(form)] = [content.strip(), label]
    contents_vector = []
    for item in form.iloc[:, 0].values:
        value = item.split(',')
        array = []
        for item2 in value:
            b = int2bin(int(item2), 32)
            for c in b:
                array.append(int(c))
        contents_vector.append(array)
    array_to_mat = np.array(contents_vector)  # 数组转矩阵

    joblib.dump(array_to_mat, tf_idf_feature_path)
    model = KNeighborsClassifier(k)
    model.fit(array_to_mat, form.iloc[:, 1].values)
    joblib.dump(model, model_path)
    time_dif = get_time_dif(start_time)

    y_evaluate = model.predict(array_to_mat)
    acc_val = evaluate(y_evaluate, form.iloc[:, 1].values)
    return acc_val, time_dif


def test(test_data, save_dir):
    model_path = os.path.join(save_dir, 'trainModel.pkl')

    start_time = time.time()
    model = joblib.load(model_path)

    contents_vector = []
    array = []
    for item in test_data:
        b = int2bin(int(item), 32)
        for c in b:
            array.append(int(c))

    contents_vector.append(array)
    array_to_mat = np.array(contents_vector)  # 数组转矩阵

    y_prediction = model.predict(array_to_mat)
    time_dif = get_time_dif(start_time)

    return y_prediction, time_dif
