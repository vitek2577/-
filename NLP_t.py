from openpyxl.writer.excel import ExcelWriter

__author__ = 'Виктор'

# -*- coding: utf8 -*-
# -*- coding: cp866 -*-
import os
import csv
import string
import pandas
import re
import numpy as np;
from sklearn.cross_validation import train_test_split
from sklearn import feature_extraction, linear_model, metrics
from sklearn import metrics
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC

data = pandas.DataFrame(columns=['Author', 'Text'])
test_text = pandas.DataFrame(columns=['Author', 'Text'])
i = 0
f = open('D:\\test\\test.txt', 'r')
newText_test = ''
for line in f.read():
    line = line.lower()
    line = re.sub("[^а-я]", " ", line)
    line = re.sub("ё", "е", line)
    newText_test = newText_test + line
test_text.loc[1] = ['', newText_test]
print(test_text)

for top, dirs, files in os.walk('D:\project\Books\Books'):
    for nm in files:
        f = open(os.path.join(top, nm), 'r')
        print(os.path.join(top, nm))
        newText = ''
        for line in f.read():
            line = line.lower()
            line = re.sub("[^а-я]", " ", line)
            line = re.sub("ё", "е", line)
            newText = newText + line
        data.loc[i] = [top.replace('D:\project\Books\Books\\', ''), newText]
        i = i + 1
        if (i == 845):
            vectorizer = feature_extraction.text.CountVectorizer(token_pattern=r'\b\w+\b', encoding = 'windows-1251')
            train_matrix = vectorizer.fit_transform(data['Text'])
            test_matrix = vectorizer.transform(test_text['Text'])
            print(test_matrix)
            model = KNeighborsClassifier()
            model.fit(train_matrix, data['Author'])
            predicted = model.predict(test_matrix)
            print(predicted)
            #print(metrics.classification_report(test['Author'], predicted))
            # print(metrics.confusion_matrix(train['Text'],predicted))
            exit()
