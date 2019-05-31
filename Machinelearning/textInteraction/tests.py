# -*- coding: utf-8 -*-
from sklearn.feature_extraction.text import CountVectorizer

X_test = ['001101000', '0 0 1 0 0 0 1 0 1']

count_vec = CountVectorizer()
print(count_vec.fit_transform(X_test).toarray())
print(count_vec.fit_transform(X_test))
print('\nvocabulary list:\n')
for key,value in count_vec.vocabulary_.items():
    print(key)
    print(value)
