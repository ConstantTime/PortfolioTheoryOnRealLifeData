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
files = os.listdir()
n = len(files)
cur_file = 1

company_names = {}

def getCompanyName(s) :
    s = s[13:]
    ans = ''
    for i in range(0 , len(s)) :
        if(s[i] == '-') :
            break
        else :
            ans = ans + s[i]
            
    return ans

for i in range(0 , n) :
    if(files[i].startswith('Quote')) :
        new_name = 'main_'
        new_name = new_name + str(cur_file)
        cur_file = cur_file + 1
        new_name = new_name + '.csv'
        os.rename(files[i] , new_name)
        company_names[new_name] = files[i]
        files[i] = new_name

for i in range(0 , n) :
    real = company_names[files[i]]
    company_names[files[i]] = getCompanyName(real) 
        
p_size = n - 1
open_list = []
close_list = []

for i in range(0 , p_size) :
    frame = pd.read_csv(files[i])
    frame.columns = frame.columns.str.strip()
    if(type(frame['OPEN'][0]) == str) :
        frame['OPEN'] = frame['OPEN'].str.replace(',' , '').astype(float)
    if(type(frame['close'][0]) == str) :
        frame['close'] = frame['close'].str.replace(',' , '').astype(float)
    frame = frame.iloc[: , [0 , 2 , 7]]
    end = len(frame)
    open_l = (np.array(frame['OPEN'][1:end]) - np.array(frame['OPEN'][0:end - 1])) / np.array(frame['OPEN'][0:end - 1])  
    close_l = (np.array(frame['close'][1:end]) - np.array(frame['close'][0:end - 1])) / np.array(frame['close'][0:end - 1])  
    open_list.append(open_l)
    close_list.append(close_l)
    
C = np.cov(open_list)
m = []
for i in range(0 , p_size) :
    m.append(np.mean(open_list[i]))

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