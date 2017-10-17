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
import nltk
import zipfile

# чистим текст оставляя только маленькие русские буквы
def clear_line (line):
     line = line.lower()
     line = re.sub("[^а-я]"," ",line )
     return line


# сохраняем тексты
def save_text (path, name):
    i = 0
    data0 = pandas.DataFrame(columns=['Author', 'Text'])
    for top, dirs, files in os.walk(path):
        for nm in files:
            f = open(os.path.join(top,nm),'r')
            newText = ''
            for line in f.read():
                line = clear_line(line)
                newText = newText + line
            newText = re.sub("\s+", " ", newText)
            k = top.replace(path,'')
            k = k.replace('\\','')
            data0.loc[i] = [k, newText]
            i += 1
    data0.to_pickle(name)
    return


def save_html (path, name):
    i = 0
    data0 = pandas.DataFrame(columns=['Author', 'Text'])
    f = open(path,'r')
    newText = ''
    for line in f.read():
        line = clear_line(line)
        newText = newText + line
        data0.loc[i] = ['', newText]
        i += 1
        newText = re.sub("\s+", " ", newText)
    data0.to_pickle(name)
    return

def load_zip (path, name):
    zf = zipfile.ZipFile(path)
    i = 0
    data0 = pandas.DataFrame(columns=['Author', 'Text'])
    for filename in zf.namelist():
        f = zf.read(filename).decode('utf-8')
        newText = ''
        for line in f:
            line = clear_line(line)
            newText = newText + line
        newText = re.sub("\s+", " ", newText)
        data0.loc[i] = ['', newText]
        i += 1
    data0.to_pickle(name)
    return



# определение автора методом косинусов
def define_author (dat, test):
    data = joblib.load(dat)
    Test = joblib.load(test)
    token = nltk.tokenize.TweetTokenizer().tokenize
    #train, test = train_test_split( data, train_size = percent, random_state = 44 ) # разделение выборки (для проверки качества)
    vectorizer = feature_extraction.text.CountVectorizer(token_pattern=r'\b\w+\b',  encoding = 'windows-1251', ngram_range=(2, 2), max_df=0.1, tokenizer= token) # max_df=0.1 уберает часто встречающиеся слова то есть наши стоп слова
    train_matrix = vectorizer.fit_transform(data['Text'])
    test_matrix = vectorizer.transform(Test['Text'])
    cos = metrics.pairwise.cosine_similarity(train_matrix, test_matrix)
    j = 0
    rigth_text = 0
    k = np.argmax(cos, axis = 0)
    Authors = []
    for elem in k:
        Authors.append(data.iloc[elem]['Author'])
        j += 1
    return Authors
        #test.iloc[j]['Author']
        #if нужен при проверки качества алгоритма
        #if train.iloc[elem]['Author'] == test.iloc[j]['Author']:
         #   rigth_text += 1
    #print (rigth_text/j*100)
