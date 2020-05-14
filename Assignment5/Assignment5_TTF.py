# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 10:25:49 2018

@author: Yang
"""

import random
import numpy as np
from scipy import stats



N = 30
alpha = 0.05


maitanence_time = 2.5
two_list = [[],[]]

def Failure(clock,last_state,state):
    
    if clock == 0 :
        next_time = clock + random.choice(range(1, 7))    
    
    if state == 0 or state > last_state:
        next_time = float("inf")
    else:
        next_time = clock + random.choice(range(1, 7))
    return next_time,-1

def Repair(clock,last_state,state):
    if state > last_state or clock == 0:
        next_time = float("inf")
    else:
        next_time = clock + maitanence_time
    return next_time,+1


for i in range(N):
    SystemState = 2 
    Clock = 0
    Last_SystemState = 0
    
    future_list = [[0,2]]
    schedule_list = []

    tool_square = 0.0
    state = 0    
        
    while SystemState > 0:
        
            
        future_list = sorted(future_list, key=lambda future_list:future_list[0])
        Clock = future_list[0][0]
        Last_SystemState = SystemState
        if Clock > 0:
            SystemState = SystemState + future_list[0][1]
            
        del future_list[0]
        
        
        NextFailure,move = Failure(Clock,Last_SystemState,SystemState)
        if NextFailure != float("inf"):
            future_list.append([NextFailure,move])
    
        NextRepair,move = Repair(Clock,Last_SystemState,SystemState)
        if NextRepair != float("inf"):
            future_list.append([NextRepair,move])   
    
        schedule_list.append([Clock,SystemState,NextFailure,NextRepair])
        tool_square += (schedule_list[state][0]- schedule_list[state-1][0])*schedule_list[state-1][1]
        state += 1
    #print np.array(schedule_list)
    two_list[0].append(schedule_list[state-1][0])
    two_list[1].append(tool_square/schedule_list[state-1][0])


df = N-1
t_val = 1-(alpha)/2
mean = [np.mean(two_list[i]) for i in range(2)]
std = [np.std(two_list[i]) for i in range(2)]
SE = [i/np.sqrt(N) for i in std]
print "Time to failure:",mean[0]
print "Average number of functional components:",mean[1]
for i in range(2):
    print mean[i]-stats.t.ppf(t_val,df)*SE[i],"< Population mean < ",mean[i]+stats.t.ppf(t_val,df)*SE[i]









