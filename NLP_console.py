#!/usr/bin/env python3
# -*- coding:  windows-1251 -*-

import os
import string
import pandas
import re
import numpy as np;
from sklearn.cross_validation import train_test_split
from sklearn import feature_extraction, metrics
from sklearn.externals import joblib
import argparse
import sys

# чистим текст оставляя только маленькие русские буквы
def clear_line (line):
     line = line.lower()
     line = re.sub("[^а-я]"," ",line )
     line = re.sub("ё", "е", line)
     return line

# сохраняем тексты
def save_text (path, path_save, amount):
    i = 0
    data0 = pandas.DataFrame(columns=['Author', 'Text'])
    for top, dirs, files in os.walk(path):
        for nm in files:
            f = open(os.path.join(top,nm),'r')
            newText = ''
            for line in f.read():
                line = clear_line(line)
                newText = newText + line
            data0.loc[i] = [top.replace(path,''), newText]
            i += 1
            if i == amount:
                data0.to_pickle(path_save)
                return

# определение автора методом косинусов
def define_author (data, test_text):
    train, test = train_test_split( data, train_size = 0.8, random_state = 44 ) # разделение выборки (для проверки качества)
    vectorizer = feature_extraction.text.CountVectorizer(token_pattern=r'\b\w+\b',  encoding = 'windows-1251', ngram_range=(2, 2), max_df=0.1) # max_df=0.1 уберает часто встречающиеся слова то есть наши стоп слова
    train_matrix = vectorizer.fit_transform(train['Text'])
    test_matrix = vectorizer.transform(test['Text'])
    cos = metrics.pairwise.cosine_similarity(train_matrix, test_matrix)
    j = 0
    rigth_text = 0
    k = np.argmax(cos, axis = 0)
    for elem in k:
        print (train.iloc[elem]['Author'])
        #if нужен при проверки качества алгоритма
        if train.iloc[elem]['Author'] == test.iloc[j]['Author']:
            rigth_text += 1
        j += 1
    print (rigth_text/165*100)


#data1 = pandas.DataFrame(columns=['Author', 'Text'])
#test_text = pandas.DataFrame(columns=['Author', 'Text'])

#save_text('D:\project1.1\Books\\','D:\project1.1\data.txt', 825) # сохраняем выборку
#save_text('D:\\test','D:\\project1.1\\test.txt', 1) # сохраняем тестовый текст

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument ('save_data')
    parser.add_argument ('save_text')
    parser.add_argument ('define_author')
    namespace = parser.parse_args(sys.argv[1:])

    if namespace.command == "save_data":
        print("Enter path")
        path = input()
        print("Enter path to save data")
        path_save = input()
        print("Enter amount of texts")
        amount = input()
        save_text(path,path_save,amount)
    if namespace.command == "save_data":
        print("Enter path")
        path = input()
        print("Enter path to save data")
        path_save = input()
        print("Enter amount of texts")
        amount = input()
        save_text(path,path_save,amount)
    if namespace.command == "define_author":
        path = input("Enter path to data ")
        path_test  = input("Enter path to text")
        data1 = joblib.load(path)
        test_text = joblib.load(path_test)
        define_author(data1, test_text)