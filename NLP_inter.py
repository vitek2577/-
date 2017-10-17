#!/usr/bin/env python3
# -*- coding:  windows-1251 -*-
from tkinter import *
from tkinter.filedialog import askdirectory, askopenfiles
from NLP import *
import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup




def result(self):
    text_field = Text()
    root = Tk()
    tx = Text(root, font=('times',12),width=50,height=15,wrap=WORD)
    tx.pack(expand=YES,fill=BOTH)
    i = 1
    for elem in self.Authors:
        tx.insert(1.0, elem)
        tx.insert(1.0, i)
        tx.insert(1.0, "№")
        tx.insert(1.0, '\n')
        text_field.pack()
        i += 1
    mainloop()

def html_read(url):
    html = urlopen(url)
    page = html.read().decode('utf-8')
    fh=open('html.txt','w')
    fh.write(page)

class directory_seeker:
    def __init__(self):
        self.root=Tk()

        self.but1=Button(self.root,text="Загрузить выборку",command=self.Return)
        self.but1.pack()

        self.but2=Button(self.root,text="Загрузить тексты у которых нужно определить автора",command=self.Test)
        self.but2.pack()

        self.but3=Button(self.root,text="Определить авторов",command=self.Define)
        self.but3.pack()

        self.but4=Button(self.root,text="Загрузка архива с определяемыми авторами",command=self.zip_T)
        self.but4.pack()

        self.but5=Button(self.root,text="Загрузка текста из интернета",command=self.web_T)
        self.but5.pack()

        self.lab = Label(self.root, text="Введите адрес страницы.", font="Arial 10")
        self.ent1 = Entry(self.root,width=20,bd=3)

        self.root.mainloop()

    def Return(self):
        self.Path_data = askdirectory()
        save_text(self.Path_data, "load.txt")

    def Test(self):
        self.T = askdirectory()
        save_text(self.T, "Test.txt")

    def Define(self):
        self.Authors = define_author("load.txt", "Test.txt")
        result(self)

    def zip_T(self):
        self.zip_test = askopenfiles()
        load_zip(self.zip_test, 'Test.txt')
    def web_T(self):
        hl = self.ent1.get()
        self.ent1.pack()
        html_read(hl)
        save_html("html.txt", "Test.txt")






dir = directory_seeker()
