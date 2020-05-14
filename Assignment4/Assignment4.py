# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 00:05:47 2018

@author: user
"""
import copy
import numpy as np
np.set_printoptions(threshold=np.nan)
all_move = []
clock = 0.0
server = 0
queue = 0
arrival_people = 0
departures_people = 0
people = [[0.4,2.0],[1.2,0.7],[0.5,0.2],[1.7,1.1],[0.2,3.7],[1.6,0.6],[0.2,1.0],[1.4,3.0],[1.9,2.5],[2.0,1.3]]

accumulative_arrival = 0
future_list = []
arrival_list = []
departures_list = []
departures_time_list  = []
accumulative_severed = 0
severed_list = []
severed_list2 = []
queue_list = []
accumulative_queue = 0


operating_time = 120.0
lam = 3.0
scale = 6.0
system_number = 0.0
leave_people = 0.0

queue_square = 0.0
system_square = 0.0

served_system_time = 0.0
served_queue_time = 0.0
state = 0
NoIdle_time = 0.0
while leave_people < 5:
    
    if clock == 0 :

        future_list.append([1,'arrivals',people[0][0]])
        departures_time_list .append(people[0][1])
        
    future_list = sorted(future_list, key=lambda future_list:future_list[2])    
    move = copy.copy(future_list[0])
    clock = move[2]
    if move[1] == "arrivals":    

        arrival_people += 1
        if server == 0 and queue == 0:
            server += 1
            accumulative_severed += 1
            severed_list.append(move[0:2])
            serving_people = move
            future_list.append([move[0],'departures',clock + departures_time_list [0]])
            del departures_time_list [0]
        else:
            queue += 1
            queue_list.append(move)
        arrival_list.append(move)
        accumulative_arrival += 1
        if arrival_people != len(people):
            future_list.append([arrival_people+1,'arrivals',clock +people[arrival_people][0]])
            departures_time_list .append(people[arrival_people][1])
       
    else:
        leave_people += 1
        server -= 1
        departures_list.append(move)
        served_system_time += move[-1]-serving_people[-1]
        served_queue_time += move[-1]-serving_people[-1] -people[move[0]-1][-1]
        if queue > 0:
            queue -= 1      
            if [move[0]]+['arrivals'] in severed_list:
                server += 1
                accumulative_severed += 1
                severed_list.append([move[0]+1,'arrivals'])
                serving_people = queue_list[0]
                del queue_list[0]
                future_list.append([move[0]+1,'departures',clock + departures_time_list [0]])
                del departures_time_list [0]


    all_move.append([server]+move+[queue])
    system_number += server+queue      
    del future_list[0]
    accumulative_queue += queue
    if len(all_move) > 1:
        queue_square += all_move[state-1][-1]*(all_move[state][-2]-all_move[state-1][-2])
        system_square += (all_move[state-1][-1]+all_move[state-1][0])*(all_move[state][-2]-all_move[state-1][-2])
        if all_move[state-1][-1]+all_move[state-1][0] > 0:
            NoIdle_time += all_move[state][-2]-all_move[state-1][-2]
    state += 1

print np.array(all_move) 
print
  
served_system_time += departures_list[-1][-1] + people[departures_list[-1][0]][-1] - serving_people[-1]
served_queue_time += departures_list[-1][-1] - serving_people[-1]
operating_time = all_move[-1][-2]
severed_number = len(severed_list)
print '(a) Average number of customers in the system:',system_square/operating_time
print '(b) Average number of customers in the queue:',queue_square/operating_time
print '(c) Average time in the system:',served_system_time/severed_number
print '(d) Average time in the queue:',served_queue_time/severed_number
print '(e) Proportion of time the server is idle:',1-NoIdle_time/operating_time

    
    
