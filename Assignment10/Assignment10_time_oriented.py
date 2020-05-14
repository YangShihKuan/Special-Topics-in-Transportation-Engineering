# -*- coding: utf-8 -*-
"""
Created on Sun Jun 03 15:53:15 2018

@author: Yang
"""




import numpy as np
import csv
import copy
data_set = []
outfile = open('c101.txt','r')
outfile.readline()
outfile.readline()
outfile.readline()
outfile.readline()
info = outfile.readline()
info = info.split()
#print info
car = int(info[0])
capacity = int(info[1])
outfile.readline()
outfile.readline()
outfile.readline()
outfile.readline()
for row in outfile:
    word = row.split()
    data_set.append(word)    
outfile.close()
data_set = [map(int,x) for x in data_set]
#print data_set
'''
with open('c101a.csv','rb') as csv_file:
    rows = csv.reader(csv_file)
    for row in rows:
        data_set.append(row)
'''        
#print data_set
capacity = 200
car = 25
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
    del temp_distant[0]        
    if i > 0:
        distant.append(temp_distant)


adjust_data = copy.copy(data_set)
adjust_data.remove(adjust_data[0])
adjust_data = sorted(adjust_data, key = lambda x : x[4])

start_sort_list = [adjust_data[i][0] for i in range(len(adjust_data))]



def find_route(sourse,start_sort_list):
    #print "------------------------------------------------------------------------",i
    start_sort_list.remove(sourse)
    temp_route_list = [sourse]
    route_time = depot_distant[sourse]+service_time[sourse]
    route_capacity = deamnd[sourse]
    #search_location = i
    #print 
    while route_capacity < capacity:
        i = temp_route_list[-1]      
        #print i
        saving_list = []
        
        for j in start_sort_list:
            if i!=j  and route_time+distant[i-1][j-1] <= due_date[j]:
                
                bj = max([ready_time[j],route_time+service_time[i]+distant[i-1][j-1]])
                Tij = bj -(route_time+service_time[i])
                vij = due_date[j]-(route_time+service_time[i]+distant[i-1][j-1])
                direct_distant = distant[i-1][j-1]/3.0 + Tij/3.0 + vij/3.0
                
                saving_list.append(direct_distant)
            else:
                saving_list.append(".")
        if len(saving_list) == 0:
            break                
        
        #print saving_list
        next_index = saving_list.index(min(saving_list))
        #print next_index
        next_customer = start_sort_list[next_index]
        #print next_customer
        for replace in range(len(saving_list)):
            if saving_list[replace] == ".":
                saving_list[replace] = 0
        #print saving_list
        if sum(saving_list) == 0:
            break          
        
        #print next_customer

        if route_capacity + deamnd[next_customer] <= capacity and route_time + distant[i-1][next_customer-1] +service_time[next_customer] <= deadline:
    
            temp_route_list.append(next_customer)
            route_capacity += deamnd[next_customer]
            #print "ready_time[next_customer]",ready_time[next_customer]
            #print "route_time+distant[i-1][next_customer-1]",route_time+distant[i-1][next_customer-1]
            route_time = max([ready_time[next_customer],route_time+distant[i-1][next_customer-1]]) +service_time[next_customer]
            #print "route_time",route_time
            start_sort_list.remove(next_customer)
            #print "-----",temp_route_list
        else:
            break
        #print '------------'
    return temp_route_list,start_sort_list



route_list = []
while len(start_sort_list) != 0:
    
    i = start_sort_list[0]
    #print i
    
    temp_route_list,start_sort_list = find_route(i,start_sort_list)
    print temp_route_list
    route_list.append(temp_route_list)

print
print len(route_list)
#print np.array(route_list)


#print "++++++++++++++++++++"

def validation(route_list):
    for route in route_list:
        time = 0
        capacity = 0
        print route
        for coustomer in range(len(route)):
            #
            if coustomer == 0:
                #print coustomer
                time += depot_distant[route[coustomer]]+service_time[route[coustomer]]
                capacity += deamnd[route[coustomer]]
                if depot_distant[route[coustomer]]>=ready_time[route[coustomer]] and depot_distant[route[coustomer]]<=due_date[route[coustomer]]:
                    print route[coustomer],"correct"
                else:
                    print route[coustomer],"worng"                
            else:
                #print 'time-----',time
       
                time = max([time+distant[coustomer-2][coustomer-1],ready_time[route[coustomer]]])
                #print 'time',time
                #print 'due_date',due_date[route[coustomer]]
                capacity += deamnd[coustomer]
                if time<=due_date[route[coustomer]]:
                    print route[coustomer],"correct"
                else:
                    print route[coustomer],"-------------------------------------worng"
            
                time +=service_time[route[coustomer]]
            
        print "last_____________time", time

#run = validation(route_list)


time = 0
for i in range(len(route_list[0])):
    
    if i  == 0:
        print depot_distant[route_list[0][i]],ready_time[route_list[0][i]],due_date[route_list[0][i]]
        time += depot_distant[route_list[0][i]] + service_time[route_list[0][i]]
    elif i  == len(route_list[0])-1:
        print time+distant[route_list[0][i]-2][route_list[0][i]-1],ready_time[route_list[0][i]],due_date[route_list[0][i]]
        time += depot_distant[route_list[0][i]] + service_time[route_list[0][i]]
        print time      
    else:
        print time+distant[route_list[0][i]-2][route_list[0][i]-1],ready_time[route_list[0][i]],due_date[route_list[0][i]]
        time = max(ready_time[route_list[0][i]],time+distant[route_list[0][i]-2][route_list[0][i]-1]) + service_time[route_list[0][i]]
















      