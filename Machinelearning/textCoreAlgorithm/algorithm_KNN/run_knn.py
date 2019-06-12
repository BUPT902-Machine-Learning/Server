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


def evaluate(y_preds, y_labels):
    num = 0
    count = 0
    for pred, label in zip(y_preds, y_labels):
        count = count + 1
        if pred == label:
            num = num + 1

    return float(num / count)


def train(contents, labels, save_dir, k):
    # 打乱样本与标签排序
    state = np.random.get_state()
    np.random.shuffle(contents)
    np.random.set_state(state)
    np.random.shuffle(labels)
    sep = int(len(contents) / 3 * 2)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    model_path = os.path.join(save_dir, 'trainModel.pkl')
    tf_idf_feature_path = os.path.join(save_dir, 'tfIdfFeature.pkl')

    start_time = time.time()
    form = pd.DataFrame(columns=['contents', 'labels'])
    for content, label in zip(contents, labels):
        form.loc[len(form)] = [content.strip(), label]
    count = CountVectorizer(tokenizer=tokenizer)
    count_vector = count.fit_transform(form.iloc[:, 0]).toarray()
    count_vector_train = count_vector[:sep]
    count_vector_val = count_vector[sep:]
    joblib.dump(count.vocabulary_, tf_idf_feature_path)
    model = KNeighborsClassifier(k)
    model.fit(count_vector_train, form.iloc[:sep, 1].values)
    joblib.dump(model, model_path)
    time_dif = get_time_dif(start_time)

    y_evaluate = model.predict(count_vector_val)
    acc_val = evaluate(y_evaluate, form.iloc[sep:, 1].values)
    return acc_val, time_dif


def test(test_data, save_dir):
    model_path = os.path.join(save_dir, 'trainModel.pkl')
    tf_idf_feature_path = os.path.join(save_dir, 'tfIdfFeature.pkl')

    start_time = time.time()
    loaded_vec = CountVectorizer(tokenizer=tokenizer, vocabulary=joblib.load(open(tf_idf_feature_path, "rb")))
    form = pd.DataFrame(columns=['content'])
    form.loc[len(form)] = [test_data.strip()]
    count_vector = loaded_vec.transform(form.iloc[:, 0]).toarray()
    index = len(count_vector)
    model = joblib.load(model_path)
    y_prediction = model.predict(count_vector[[index - 1]])
    time_dif = get_time_dif(start_time)

    return y_prediction, time_dif