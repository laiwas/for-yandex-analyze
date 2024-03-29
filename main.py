import numpy as np
import pandas as pd
import csv
import pymorphy2

#Functions

def proverka(a, b):
    if '"' in b[0]:
        return tochnaya_proverka(a, b)
    if '[' in b[0]:
        return kvadrat_proverka(a, b)
    else:
        for x in b:
            if x in a:
                continue
            else:
                return 0
        return 1

def kvadrat_proverka(a, b):
    b1 = []
    tmp = []
    for x in b:
        b1.append(x)
    b1[0] = b1[0].replace('[', '')
    b1[-2] = b1[-2].replace(']','')
    if b1[-1] in a:
        for i in range(len(b1) - 1):
            if b1[i] in a:
                tmp.append(b1[i])
            else:
                return 0
        b1.remove(b1[-1])
        for i in range(len(tmp)):
            if tmp[i] != b1[i]:
                return 0
        else:
            return 1
    else:
        return 0





def tochnaya_proverka(a, b):
    b1 = []
    for x in b:
        b1.append(x)
    b1[0] = b1[0].replace('"', '')
    b1[-1] = b1[-1].replace('"','')
    if len(a) != len(b1):
        return 0
    else:
        for elem in b1:
            if elem in a:
                continue
            else:
                return 0
        return 1


morph = pymorphy2.MorphAnalyzer()
def normed_word(x):
    p = morph.parse(x)[0]
    return p.normal_form


semantic = [] #our semantic kernal as list
searches = [] #our searches as list

#Считываем

df1 = pd.read_csv('semantic.csv', encoding='utf-8')
strings = df1['keyword_name:'].values
for row in strings:
    semantic.append(row)

df2 = pd.read_csv('searches.csv', encoding='utf-8')

strings = df2['searches'].values
for row in strings:
    searches.append(row)

semantic_saved = []  #Сохраняем семантику, чтобы потом вставлять её в файл
for x in semantic:
    semantic_saved.append(x)

#Parsing

for i in range(len(semantic)):
    semantic[i] = semantic[i].split()
    tmp=[]
    for j in range(len(semantic[i])):
        if semantic[i][j][0] == '-':
            tmp.append(semantic[i][j])
        elif semantic[i][j][0] == '+':
            semantic[i][j] = normed_word(semantic[i][j].replace('+',''))
        else:
            semantic[i][j] = normed_word(semantic[i][j])
    for x in tmp:
        semantic[i].remove(x)
print('---------!semantic parsed!---------')


for i in range(len(searches)):
    tmp=[]
    searches[i] = searches[i].split()
    for j in range(len(searches[i])):
        searches[i][j] = normed_word(searches[i][j])
print('---------!searches parsed!---------')


#Analyzing

def analyze(srch,smnt):

    list_tmp=[]
    for k in range(len(srch)):
        for i in range(len(smnt)):
            tmp = proverka(srch[k],smnt[i])
            if tmp == 0:
                continue
            else:
                list_tmp.append(semantic_saved[i])
                if k%1000 == 0:
                    print('complete ', k,' from all')
                break
        else:
            list_tmp.append('Unknown')
            if k%1000 == 0:
                print('complete ', k, ' from all')
    return list_tmp


df2['predictions'] = analyze(searches, semantic)
df2.to_csv('result_active_searches_old_semantic.csv')