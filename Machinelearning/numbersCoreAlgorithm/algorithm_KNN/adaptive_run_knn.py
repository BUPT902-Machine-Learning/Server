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


def get_time_dif(start_time):
    """获取已使用时间"""
    end_time = time.time()
    time_dif = end_time - start_time
    return timedelta(seconds=int(round(time_dif)))


def tokenizer(s):
    words = []
    cut = jieba.cut(s)
    for word in cut:
        words.append(word)
    return words


def evaluate(y_preds, y_labels):
    num = 0
    count = 0
    for pred, label in zip(y_preds, y_labels):
        count = count + 1
        if pred == label:
            num = num + 1

    return float(num/count)


def train(contents, labels, modelName):
    save_dir = 'checkpoints/' + modelName
    os.makedirs(save_dir)
    model_save = os.path.join(save_dir, 'train_model')
    print(contents)
    print(labels)
    start_time = time.time()
    corpos = pd.DataFrame(columns=['contents', 'labels'])
    for content, label in zip(contents, labels):
        corpos.loc[len(corpos)] = [content.strip(), label]

    corpos = corpos.sample(frac=1)
    count = CountVectorizer(tokenizer=tokenizer)
    countvector = count.fit_transform(corpos.iloc[:, 0]).toarray()

    left = int(len(contents) / 3)
    sep = len(contents) - left
    countvector1 = countvector[:sep]
    countvector2 = countvector[sep:]
    model = KNeighborsClassifier(5)
    model.fit(countvector1, corpos.iloc[:sep, 1].values)
    joblib.dump(model, model_save)
    time_dif = get_time_dif(start_time)
    y_evaluate = model.predict(countvector2)
    eval = evaluate(y_evaluate, corpos.iloc[sep:, 1].values)
    return 1, eval, time_dif


def test(contents, modelName):
    model_save = 'checkpoints/' + modelName + '/train_model'
    start_time = time.time()
    print(contents)
    corpos = pd.DataFrame(columns=['content'])
    for content in contents:
        corpos.loc[len(corpos)] = [content.strip()]
    count = CountVectorizer(tokenizer=tokenizer)
    countvector = count.fit_transform(corpos.iloc[:, 0]).toarray()
    index = len(countvector)
    model = joblib.load(model_save)
    y_pred = model.predict(countvector[[index - 1]])
    time_dif = get_time_dif(start_time)
    return y_pred, time_dif
