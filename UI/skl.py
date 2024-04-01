from config import *
import numpy as np
import re
import jieba
from jieba import posseg
import os
import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from UI.models import RootData


# 从数据库中读取数据


# 处理数据
def text_process(text):
    words = posseg.cut(text)
    words = [word.word for word in words if word.flag.startswith('n')]  # 只保留名词
    stop_words = [line.strip() for line in open('stopwords.txt', encoding='utf-8').readlines()]  # 加载停用词
    words = [word for word in words if word not in stop_words]
    return ' '.join(words)


def skl():
    data = RootData.objects.all()

    # 处理数据
    X = np.array([text_process(item.text) for item in data])
    y = np.array([item.label for item in data])

    # 将文本转化为特征向量
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(X)

    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # 定义朴素贝叶斯分类器
    clf = MultinomialNB()

    # 训练模型
    clf.fit(X_train, y_train)

    # 预测
    y_pred = clf.predict(X_test)

    # 计算准确率
    accuracy = accuracy_score(y_test, y_pred)
    print('准确率：', accuracy)
