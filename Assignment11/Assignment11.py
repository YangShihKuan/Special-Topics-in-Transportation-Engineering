# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 20:17:55 2018

@author: Yang
"""

import numpy as np
import csv
import copy

data_set = []
outfile = open('c107.txt','r')
for i in range(4):
    outfile.readline()
info = outfile.readline()
info = info.split()
car = int(info[0])
capacity = int(info[1])
for i in range(4):
    outfile.readline()
for row in outfile:
    word = row.split()
    data_set.append(word)    
outfile.close()
data_set = [map(int,x) for x in data_set]

distant=[];xy=[];coordinate={};deamnd={};ready_time={};due_date={};service_time={}

depot_distant={}
deadline = 0

for i in data_set:
    xy.append([i[1],i[2]])
    if i[0] == 0:
        deadline = i[5]
    if i[0] > 0:
        
        coordinate[i[0]] = [i[1],i[2]]
        deamnd[i[0]] = i[3]
        ready_time[i[0]] = i[4]
        due_date[i[0]] = i[5]
        service_time[i[0]] = i[6]

for i in range(len(xy)):
    temp_distant = []
    for j in range(len(xy)):
        dddistant =  np.sqrt((xy[i][0]-xy[j][0])**2+(xy[i][1]-xy[j][1])**2)
        temp_distant.append(dddistant)
        if i == 0 and j>0:
            depot_distant[j] =  dddistant
    #del temp_distant[0]        

    distant.append(temp_distant)


def check_feasible_route(feasible_route):
    
    debug1 = 0
    debug2 = 0    
    debug_time = 0
    
    debug_route_time = []
    debug_real_time = []
    for i in range(len(feasible_route)):
        if i == 0:
            debug_route_time.append(0)
            debug_real_time.append(0)
        elif i == len(feasible_route)-1:

            debug_time = debug_time+distant[feasible_route[i-1]][feasible_route[i]]
            debug_route_time.append(debug_time)
            debug_real_time.append(deadline)
            
        elif i > 0:

            debug_time = max([debug_time+distant[feasible_route[i-1]][feasible_route[i]],ready_time[feasible_route[i]]])
            debug_route_time.append(debug_time)
            debug_real_time.append(due_date[feasible_route[i]])
            debug_time += service_time[feasible_route[i]]
            
    for i,j in zip(debug_route_time,debug_real_time):
        if  i > j:
            debug1 = 1
    if debug_time > deadline:
        debug2 = 1   
    debug_signal = debug1 + debug2
    
    return debug_signal


adjust_data = copy.copy(data_set)
adjust_data.remove(adjust_data[0])
adjust_data = sorted(adjust_data, key = lambda x : x[4])

customer_list = [adjust_data[i][0] for i in range(len(adjust_data))]
route_all = []
while len(customer_list) != 0:
    route_list = [0,0]
    insert_customer = customer_list[int((len(customer_list))/2)]
    route_list.insert(1,insert_customer)
    customer_list.remove(insert_customer)
    
    route_capacity = 0
    while route_capacity < capacity:
        customer_c1_value = []
        customer_c1_place = []
        
        survive_customer_list = copy.copy(customer_list)
        for customer in customer_list:
            
            c1_value = []
            c1_place = []
            
            for place in range(1,len(route_list)):
                
                test_list = copy.copy(route_list)
                test_list.insert(place,customer)
                #check the feasible
                debug_signal = check_feasible_route(test_list)
                #print test_list
                i_customer = test_list[place-1]
                j_customer = test_list[place+1]
                #print customer
                #print i_customer
                #print j_customer
                c1 = 0
                if debug_signal == 0:
                    c1 = distant[i_customer][customer] + distant[customer][j_customer] - distant[i_customer][j_customer]
                    
                    c1_value.append(c1)
                    c1_place.append(place)
        
        
            #print c1_value 
            #print c1_place
            if len(c1_value) > 0:
                mini_value = min(c1_value)
                mini_index = c1_value.index(mini_value)
                customer_c1_value.append(mini_value)
                customer_c1_place.append(c1_place[mini_index])
            else:
                survive_customer_list.remove(customer)  
        if len(customer_c1_place) == 0:
            break

        c2_list = []
        
        for index,customer in enumerate(survive_customer_list):
            #print index
            c2_list.append(distant[0][customer]-customer_c1_value[index])
        #print c2_list
        best_c2 = max(c2_list)

        best_place = customer_c1_place[c2_list.index(best_c2)]
        best_customer = survive_customer_list[c2_list.index(best_c2)]
        #print "best_customer",best_customer
        route_list.insert(best_place,best_customer)
        route_capacity += deamnd[best_customer]
        
        customer_list.remove(best_customer)
    #print route_list
    #print check_feasible_route(route_list)
    route_all.append(route_list)
print np.array(route_all  )
print len(route_all)  
