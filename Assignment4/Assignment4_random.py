# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 00:05:47 2018

@author: user
"""
import copy
import numpy as np
np.set_printoptions(threshold=np.nan)

clock = 0.0
server = 0
queue = 0

accumulative_severed = 0
accumulative_arrival = 0
accumulative_queue = 0
arrival_interval = 0
service_time = 0

lam = 6.0 #service_time
scale = 3.0 #arrival_interval
departures_list = []
event_list = []
departures_time_list  = []
severed_list = []
all_move = []

people = []
operating_time = 50

queue_list = []
queue_square = 0.0
system_square = 0.0

served_system_time = 0.0
served_queue_time = 0.0
state = 0
NoIdle_time = 0.0

while clock < operating_time:
    
    if clock == 0 : #sever= 0 queue = 0 clock = 0 first people come first future event append
        arrival_interval = np.random.exponential(scale)
        service_time = np.random.exponential(lam)
        people.append([arrival_interval,service_time])
        event_list.append([accumulative_arrival+1,'arrivals',clock+arrival_interval])
        departures_time_list .append(people[accumulative_arrival][1])      
    event_list = sorted(event_list, key=lambda event_list:event_list[2])    
    move = copy.copy(event_list[0])
    clock = move[2] # update time
    if clock < operating_time:
        if move[1] == 'arrivals':
            if server == 0 and queue == 0:
                #server,accumulative_severed,severed_list,departures_time_list ,event_list =  Next_departures(server,accumulative_severed,move,severed_list,clock,departures_time_list )       
                server += 1
                accumulative_severed += 1
                severed_list.append([move[0],'arrivals']) # arrange to severed list
                serving_people = move
                event_list.append([move[0],'departures',departures_time_list [0]+clock])
                del departures_time_list [0] 
            else:
                queue += 1  
                queue_list.append(move)
            accumulative_arrival += 1
            #arrival_interval,service_time,people,event_list,departures_time_list  = Next_arrival(arrival_interval,service_time,people,event_list,accumulative_arrival,clock,departures_time_list )      
            arrival_interval = np.random.exponential(scale)
            service_time = np.random.exponential(lam)
            people.append([arrival_interval,service_time])
            event_list.append([accumulative_arrival+1,'arrivals',clock+arrival_interval])
            departures_time_list .append(people[accumulative_arrival][1])              
        else:
            departures_list.append(move)
            server -= 1
            served_system_time += move[-1]-serving_people[-1]
            served_queue_time += move[-1]-serving_people[-1] -people[move[0]-1][-1]
            if queue > 0:
                queue -= 1
                if [move[0]]+['arrivals'] in severed_list:
                    #server,accumulative_severed,severed_list,departures_time_list ,event_list =  Next_departures(server,accumulative_severed,move,severed_list,clock,departures_time_list )  
                    server += 1
                    accumulative_severed += 1
                    severed_list.append([move[0]+1,'arrivals']) # arrange to severed list
                    serving_people = queue_list[0]
                    del queue_list[0]                    
                    event_list.append([move[0]+1,'departures',departures_time_list [0]+clock])
                    del departures_time_list [0]        
    
        all_move.append([server]+move+[queue])

        del event_list[0]
        accumulative_queue += queue
        if len(all_move) > 1:
            queue_square += all_move[state-1][-1]*(all_move[state][-2]-all_move[state-1][-2])
            system_square += (all_move[state-1][-1]+all_move[state-1][0])*(all_move[state][-2]-all_move[state-1][-2])
            if all_move[state-1][-1]+all_move[state-1][0] > 0:
                NoIdle_time += all_move[state][-2]-all_move[state-1][-2]
        state += 1

print np.array(all_move) 
print 
if len(departures_list)>0:
    served_system_time += departures_list[-1][-1] + people[departures_list[-1][0]][-1] - serving_people[-1]
    served_queue_time += departures_list[-1][-1] - serving_people[-1]
if all_move[-1][-1]+all_move[state-1][0] > 0:
    NoIdle_time += operating_time - all_move[-1][-2]

severed_number = len(severed_list)
print '(a) Average number of customers in the system:',system_square/operating_time
print '(b) Average number of customers in the queue:',queue_square/operating_time
print '(c) Average time in the system:',served_system_time/severed_number
print '(d) Average time in the queue:',served_queue_time/severed_number
print '(e) Proportion of time the server is idle:',1-NoIdle_time/operating_time