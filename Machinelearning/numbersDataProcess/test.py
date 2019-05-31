import sys
from imp import reload
import jieba
from collections import Counter

stopwords_path = "../datas/stopWords.txt"
#
# contents = ["我喜欢你", "你真漂亮", "你真好看", "你真漂亮"]
# all_data = []
# for content in contents:
#     print(content)
#     all_data.extend(content)
#     print(all_data)
# counter = Counter(all_data)
# print(counter)
# count_pairs = counter.most_common()
# print(count_pairs)
# words, _ = list(zip(*count_pairs))
# print(words)
# # 添加一个 <PAD> 来将所有文本pad为同一长度
# words = ['<PAD>'] + list(words)
# print(words)


if sys.version_info[0] > 2:
    is_py3 = True
else:
    reload(sys)
    sys.setdefaultencoding("utf-8")
    is_py3 = False


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


def move_stopwords(raw_data):
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


contents = ["我来到北京清华大学", "我喜欢你", "我更喜欢北京大学"]
participle_data = []

for content in contents:
    seg_list = jieba.cut(content, cut_all=False)
    participle_data.append(list(seg_list))

print(participle_data)
vocab_data, all_data = move_stopwords(participle_data)
print(vocab_data)
print(all_data)

counter = Counter(all_data)
count_pairs = counter.most_common(4999)
words, _ = list(zip(*count_pairs))
# 添加一个 <PAD> 来将所有文本pad为同一长度
words = ['<PAD>'] + list(words)
open_file("text.txt", mode='w').write('\n'.join(words) + '\n')

# words = open_file(vocab_dir).read().strip().split('\n')
with open_file("text.txt", mode='r') as fp:
    # 如果是py2 则每个值都转化为unicode
    words = [native_content(_.strip()) for _ in fp.readlines()]
word_to_id = dict(zip(words, range(len(words))))
print(words)
print(word_to_id)
