# coding: utf-8

import sys
from collections import Counter

import numpy as np
import tensorflow.contrib.keras as kr
import jieba
from imp import reload

stopwords_path = "data/stopWords.txt"

if sys.version_info[0] > 2:
    is_py3 = True
else:
    reload(sys)
    sys.setdefaultencoding("utf-8")
    is_py3 = False


def native_word(word, encoding='utf-8'):
    """如果在python2下面使用python3训练的模型，可考虑调用此函数转化一下字符编码"""
    if not is_py3:
        return word.encode(encoding)
    else:
        return word


def native_content(content):
    if not is_py3:
        return content.decode('utf-8')
    else:
        return content


def open_file(filename, mode='r'):
    """
    常用文件操作，可在python2和python3间切换.
    mode: 'r' or 'w' for read or write
    """
    if is_py3:
        return open(filename, mode, encoding='utf-8', errors='ignore')
    else:
        return open(filename, mode)


def move_stop_word(word):
    stopwords = [line.strip() for line in open_file(stopwords_path).readlines()]
    if word not in stopwords:
        if word != '\t'and'\n':
            return True
    return False


def move_stop_words(raw_data):
    stopwords = [line.strip() for line in open_file(stopwords_path).readlines()]
    stop_str = []
    stop_all_str = []
    for item in raw_data:
        sentence = []
        for word in item:
            if word not in stopwords:
                if word != '\t'and'\n':
                    stop_str.append(word)
                    sentence.append(word)

        stop_all_str.append(sentence)
    return stop_str, stop_all_str


def build_vocab(contents, vocab_dir, vocab_size=5000):
    """根据训练集构建词汇表，存储"""
    participle_data = []
    for content in contents:
        seg_list = jieba.cut(content, cut_all=False)
        participle_data.append(list(seg_list))

    vocab_data, all_data = move_stop_words(participle_data)
    counter = Counter(vocab_data)
    count_pairs = counter.most_common(vocab_size - 1)
    words, _ = list(zip(*count_pairs))
    # 添加一个 <PAD> 来将所有文本pad为同一长度
    words = ['<PAD>'] + list(words)
    open_file(vocab_dir, mode='w').write('\n'.join(words) + '\n')
    return all_data


def participle_test_data(test_data):
    participle_data = []
    seg_list = jieba.cut(test_data, cut_all=False)
    participle_data.append(list(seg_list))

    _, all_data = move_stop_words(participle_data)
    return all_data[0]


def read_vocab(vocab_dir):
    """读取词汇表"""
    # words = open_file(vocab_dir).read().strip().split('\n')
    with open_file(vocab_dir) as fp:
        # 如果是py2 则每个值都转化为unicode
        words = [native_content(_.strip()) for _ in fp.readlines()]
    word_to_id = dict(zip(words, range(len(words))))
    return words, word_to_id


def read_category(labels):
    """读取分类目录，固定"""
    categories = labels

    categories = [native_content(x) for x in categories]

    cat_to_id = dict(zip(categories, range(len(categories))))

    return categories, cat_to_id


def to_words(content, words):
    """将id表示的内容转换为文字"""
    return ''.join(words[x] for x in content)


def process_train_data(contents, labels, word_to_id, cat_to_id, max_length=20):
    data_id, label_id = [], []

    for i in range(len(contents)):
        data_id.append([word_to_id[x] for x in contents[i] if x in word_to_id])
        label_id.append(cat_to_id[labels[i]])

    # 使用keras提供的pad_sequences来将文本pad为固定长度
    x_pad = kr.preprocessing.sequence.pad_sequences(data_id, max_length)
    y_pad = kr.utils.to_categorical(label_id, num_classes=len(cat_to_id))  # 将标签转换为one-hot表示

    return x_pad, y_pad


def process_test_data(test_data, word_to_id, max_length=20):
    data_id = []
    data_id.append([word_to_id[x] for x in test_data if x in word_to_id])
    # 使用keras提供的pad_sequences来将文本pad为固定长度
    x_pad = kr.preprocessing.sequence.pad_sequences(data_id, max_length)
    print(x_pad)
    return x_pad


def batch_iter(x, y, batch_size):
    """生成批次数据"""
    data_len = len(x)
    num_batch = int((data_len - 1) / batch_size) + 1

    indices = np.random.permutation(np.arange(data_len))
    x_shuffle = x[indices]
    y_shuffle = y[indices]

    for i in range(num_batch):
        start_id = i * batch_size
        end_id = min((i + 1) * batch_size, data_len)
        yield x_shuffle[start_id:end_id], y_shuffle[start_id:end_id]
