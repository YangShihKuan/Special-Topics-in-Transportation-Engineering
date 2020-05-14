# -*- coding: utf-8 -*-
"""
Created on Tue Jun 26 16:56:39 2018

@author: Kuan
"""
import numpy as np
import copy
import os
import time
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
        #print i,j
        if  i > j:
            debug1 = 1
    if debug_time > deadline:
        debug2 = 1   
    debug_signal = debug1 + debug2
    
    return debug_signal



def route_finder(Hroute_list,customer_list):
    route_all = []
    while len(customer_list) != 0:
        route_list = copy.copy(Hroute_list)
        #insert_customer = customer_list[0]
        insert_customer = customer_list[int((len(customer_list))/2)]
        route_list.insert(1,insert_customer)
        customer_list.remove(insert_customer)
        route_capacity = 0
        while route_capacity < capacity*0.6:
            customer_c1_value = []
            customer_c1_place = []
            survive_customer_list = copy.copy(customer_list)
            for customer in customer_list:
                c1_value = []
                c1_place = []                
                for place in range(1,len(route_list)):
                    test_list = copy.copy(route_list)
                    test_list.insert(place,customer)
                    debug_signal = check_feasible_route(test_list)
                    i_customer = test_list[place-1]
                    j_customer = test_list[place+1]
                    c1 = 0
                    if debug_signal == 0:
                        c1 = distant[i_customer][customer] + distant[customer][j_customer] - distant[i_customer][j_customer]
                        
                        c1_value.append(c1)
                        c1_place.append(place)
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
                c2_list.append(distant[0][customer]-customer_c1_value[index])
            best_c2 = max(c2_list)
            best_place = customer_c1_place[c2_list.index(best_c2)]
            best_customer = survive_customer_list[c2_list.index(best_c2)]
            route_list.insert(best_place,best_customer)
            route_capacity += deamnd[best_customer]
            customer_list.remove(best_customer)

        route_all.append(route_list)
    return route_all
def route_finder2(asd,input_all_customer):
    new_route = []
    for i in range(len(asd)):
        original_route = asd[i]
        change_route = [0]+asd[i]+[0]
        route_capacity = 0
        while route_capacity < capacity:
            customer_c1_value = []
            customer_c1_place = []  
            survive_customer_list = copy.copy(input_all_customer)        
            for customer in input_all_customer:
                c1_value = []
                c1_place = []    
    
                for place in range(len(original_route)+1,len(change_route)):
                    test_list = copy.copy(change_route)
                    test_list.insert(place,customer)
                    debug_signal = check_feasible_route(test_list)
                    i_customer = test_list[place-1]
                    j_customer = test_list[place+1]
                    c1 = 0
                    if debug_signal == 0:
                        c1 = distant[i_customer][customer] + distant[customer][j_customer] - distant[i_customer][j_customer]
                        
                        c1_value.append(c1)
                        c1_place.append(place)          
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
                c2_list.append(distant[0][customer]-customer_c1_value[index])
            best_c2 = max(c2_list)
            best_place = customer_c1_place[c2_list.index(best_c2)]
            best_customer = survive_customer_list[c2_list.index(best_c2)]

            change_route.insert(best_place,best_customer)
            input_all_customer.remove(best_customer)
            route_capacity += deamnd[best_customer]      
        new_route.append(change_route)

    new_car = route_finder(aroute_list,input_all_customer) 
    new_asd = asd+[[]]*len(new_car)
    return new_asd,new_route+new_car

def planmaker(acar_plan,aunknow_car_schedule):
    acar_schedule = []
    for a_plan in range(len(acar_plan)):
    
        running_route = acar_plan[a_plan]  
        running_time = 0
        for i in range(1,len(running_route)):
            acar_schedule.append([a_plan+1,running_time,acar_plan[a_plan][i]])
            if i == len(running_route)-1:
                running_time = running_time+distant[running_route[i-1]][running_route[i]]
            elif i > 0:
                running_time = max([running_time+distant[running_route[i-1]][running_route[i]],ready_time[running_route[i]]])
                running_time += service_time[running_route[i]]
    all_car_schedule = acar_schedule + aunknow_car_schedule
    all_car_schedule = sorted(all_car_schedule, key = lambda x : (x[1],x[0]))
    return all_car_schedule
################################################################################# 
start_time = time.clock()
all_car = 0
all_dist = 0
path='.'
files=os.listdir(path)
dddddddddddddd = 0
for f in files:
    dddddddddddddd+=1
    if dddddddddddddd==16:
        break
    data_set = [];unknow_data_set = []
    xy=[];distant=[];#depot_distant={}
    deamnd={};ready_time={};due_date={};service_time={}
    n = 0
    Known_lower= 0
    Known_upper = 0
    Unknown_lower = 0
    Unknown_upper = 0
    
    outfile = open(f)
    for row in outfile:
        word = row.split()
        if len(word) != 0:
            if word[0] == 'Known':
                Known_lower = n+1
                Known_upper = Known_lower + 1 + int(word[2])
            elif word[0] == 'Unknown':
                Unknown_lower = n+1
                Unknown_upper = Unknown_lower + 1 + int(word[2])
        if n == 0:
            capacity = 200
            vehicles = int(word[8])
            Customers = int(word[1])
        elif n < 104 and n > 2:
            xy.append([int(word[1]),int(word[2])])
            if word[0] == 'D':
                deadline = int(word[5])
                deamnd[0] = 0
        elif n > Known_lower and n < Known_upper:
            who = int(word[0])+1
            data_set.append([who,int(word[2]),int(word[3])])
            ready_time[who] =int(word[2])
            due_date[who] = int(word[3])
            deamnd[who] = int(word[4])
            service_time[who] = int(word[5])
        elif n > Unknown_lower and n < Unknown_upper:
            who = int(word[0])+100+1
            unknow_data_set.append([who,int(word[1]),int(word[2]),int(word[3]),int(word[4]),int(word[5])])
            ready_time[who] = int(word[1])
            ready_time[who] = int(word[2])
            due_date[who] = int(word[3])
            deamnd[who] = int(word[4])
            service_time[who] = int(word[5])     
    
        n += 1
    
    outfile.close()
    
    for i in range(100):
        xy.append([0,0])
    for appendcor in unknow_data_set:
     
        xy[appendcor[0]] = xy[appendcor[0]-100]
    
    for i in range(len(xy)):
        temp_distant = []
        for j in range(len(xy)):
            dddistant =  np.sqrt((xy[i][0]-xy[j][0])**2+(xy[i][1]-xy[j][1])**2)
            temp_distant.append(dddistant)
            #if i == 0 and j>0:
                #depot_distant[j] =  dddistant       
        distant.append(temp_distant)
    ##############
    #adjust_data = copy.copy(data_set)
    #data_set = sorted(data_set, key = lambda x : x[2])
    ccustomer_list = [data_set[i][0] for i in range(len(data_set))]
    aroute_list = [0,0]
    innitial_plan = route_finder(aroute_list,ccustomer_list)
    
    unknow_car_schedule = []
    for inserr_plan in unknow_data_set:
        unknow_car_schedule.append([0,inserr_plan[1],inserr_plan[0]])
    
    #changable_plan = copy.deepcopy(innitial_plan)
    car_schedule = planmaker(innitial_plan,unknow_car_schedule)
    
    car_final_route = [[]]*len(innitial_plan)
    all_movement=[]
    all_customer = [data_set[i][0] for i in range(len(data_set))]
    
    while sum(all_customer) != 0:   
        movement = copy.copy(car_schedule[0])
        all_movement.append(movement)    
        car_schedule.remove(movement)
        signal = movement[0]
        if signal == 0:
            #insert_customer = movement[2]
            all_customer.append(movement[2])
            input_all_customer = copy.copy(all_customer)
            car_final_route,new_plan = route_finder2(car_final_route,input_all_customer)
            unknow_car_schedule.remove(movement)
            car_schedule = planmaker(new_plan,unknow_car_schedule)
            for no  in all_movement:
                if no in car_schedule:
                    car_schedule.remove(no)
        else:
            car_number = movement[0]-1
            next_customer = movement[2]
            if next_customer!=0:
                all_customer.remove(next_customer)
                new_car_route = copy.copy(car_final_route[car_number])
                new_car_route.append(next_customer)
                car_final_route[car_number] = new_car_route
            
    
    total_car = len(car_final_route)
    total_dist = 0
    for i in car_final_route:
        i = [0]+i+[0]
        for j in range(len(i)):
            if j!= 0:
                total_dist += distant[j-1][j]
    #print total_car
    #print total_dist
    all_car += total_car
    all_dist +=total_dist
end_time = time.clock()
print
print "    Total Distance:",all_dist
print "      Vehicle Used:",all_car
print "Computational Time:",end_time-start_time

