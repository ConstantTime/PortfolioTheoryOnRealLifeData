# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 22:06:28 2020

@author: Rakshit
"""

import os
import pandas as pd
from numpy.linalg import inv
import numpy as np
from os import listdir
from os.path import isfile, join

def getCompanyName(s) :
    ans = "";
    for i in range(0 , len(s)) :
        if(s[i] == '.'):
            break
        ans = ans + s[i]
    return ans        

# Initialisation of variables
files = os.listdir('E:\Deep Learning\stocks\Data')
n = len(files)
cur_file = 1
company_names = {}

for i in range(0 , n) :
    name = 'main_'
    new_path = r'E:\Deep Learning\stocks\updated_names\main_'
    new_path = new_path + str(cur_file)
    name = name + str(cur_file)
    cur_file = cur_file + 1
    new_path = new_path + '.csv'
    name = name + '.csv'
    file_path = r'E:\Deep Learning\stocks\Data\\'
    file_path += files[i]
    os.rename(file_path , new_path)
    company_names[name] = getCompanyName(files[i])
    files[i] = name

for i in range(0 , n) :
    real = company_names[files[i]]
    company_names[files[i]] = getCompanyName(real) 
        
p_size = 10
Open_list = []
max_len = 2502

for i in range(0 , p_size) :
    file_path = r'E:\Deep Learning\stocks\updated_names\\'
    file_path += files[i]
    frame = pd.read_csv(file_path)
    frame.columns = frame.columns.str.strip()
    if(type(frame['Open'][0]) == str) :
        frame['Open'] = frame['Open'].str.replace(',' , '').astype(float)
    end = len(frame)
    Open_l = (np.array(frame['Open'][1:end]) - np.array(frame['Open'][0:end - 1])) / np.array(frame['Open'][0:end - 1])  
    if(len(Open_l) != max_len) :
        zero = np.empty(max_len - end)
        zero.fill(np.mean(Open_l))
        Open_l = np.concatenate((Open_l , zero))
    Open_list.append(Open_l)
    
C = np.cov(Open_list)
m = []
for i in range(0 , p_size) :
    m.append(np.mean(Open_list[i]))

u = np.empty(p_size)
u.fill(1)
u = np.matrix(u)

# for min variance portfolio
x = np.matmul(np.matmul(u , inv(C)) , np.transpose(u))
w_minvar = np.matmul(u , inv(C)) / x.item((0 , 0))
# Min Variance Weights thus are 

weights = {}
for i in range(0 , p_size) :
    weights[company_names[files[i]]] = w_minvar.item((0 , i))