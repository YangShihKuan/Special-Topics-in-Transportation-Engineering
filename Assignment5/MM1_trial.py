# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 00:05:47 2018

@author: user
"""

import numpy as np
np.set_printoptions(threshold=np.nan)
import matplotlib.pyplot as plt
from pylab import *
import copy
import pandas as pd
from scipy import stats


#parameter_number = 3
'''
operating_time = 9000
lam = 3.0 #service_time
scale = 6.0 #arrival_interval
n = 30
alpha = 0.05
warm_up_time = 0
'''
#--------------------------------------
def MM1_trial(operating_time,lam,scale,n,alpha,arival_seed,service_seed):
    five_list = [[],[],[],[],[]]
    #parameter_list = [[3,6],[6,6],[6,5],[6,3]]
    #scale = parameter_list[parameter_number][0] #arrival_interval
    #lam = parameter_list[parameter_number][1] #service_time 
    
    lamda = scale**-1*60
    mu = 60/lam
    P = lamda /mu

    formulation = [lamda/(mu-lamda),lamda**2/mu/(mu-lamda),1/(mu-lamda)*60,P/(mu-lamda)*60,(1-P)]
    '''
    print
    print '(a) Average number of customers in the system:',lamda/(mu-lamda)
    print '(b) Average number of customers in the queue:',lamda**2/mu/(mu-lamda)
    print '(c) Average time in the system:',1/(mu-lamda)*60
    print '(d) Average time in the queue:',P/(mu-lamda)*60
    print '(e) Proportion of time the server is idle:',P**n*(1-P)
    '''
    for i in range(n):
        
        time = []
    
        L, Lq, W, Wq, Idl = [], [], [], [], []
        
        clock = 0.0
        server = 0
        queue = 0
        
        arrival_interval = 0
        service_time = 0
        
        arrival_list,departures_list,queue_list,severed_list= [],[],[],[]
        departures_time_list,temp_queue_list= [],[]
        event_list,history_list,people = [],[],[]
        
        queue_square = 0.0
        system_square = 0.0
        served_system_time = 0.0
        served_queue_time = 0.0
        state = 0
        NoIdle_time = 0.0
        
        while clock < operating_time:
            if clock == 0 : #sever= 0 queue = 0 clock = 0 first people come first future event append
                
                ai = np.random.RandomState(arival_seed )
                st = np.random.RandomState(service_seed)
                arrival_interval = ai.exponential(scale)
                service_time = st.exponential(lam)
                '''
                arrival_interval = np.random.exponential(scale)
                service_time = np.random.exponential(lam)
                '''
                people.append([arrival_interval,service_time])
                event_list.append([len(arrival_list)+1,'arrivals',clock+arrival_interval])
                departures_time_list .append(people[len(arrival_list)][1])      
            event_list = sorted(event_list, key=lambda event_list:event_list[2])    
            move = copy.copy(event_list[0])
            clock = move[2] # update time
            
            if clock < operating_time:
                if move[1] == 'arrivals':
                    arrival_list.append(move)
                    if server == 0 and queue == 0:
                        server += 1
                        serving_people = move
                        severed_list.append([move[0],'severed']) # arrange to severed list
                        event_list.append([move[0],'departures',departures_time_list[0]+clock])
                        del departures_time_list[0] 
                    else:
                        queue += 1  
                        temp_queue_list.append(move)  
                    
                    ai = np.random.RandomState(arival_seed)
                    st = np.random.RandomState(service_seed)
                    arrival_interval = ai.exponential(scale)
                    service_time = st.exponential(lam)
                    '''
                    arrival_interval = np.random.exponential(scale)
                    service_time = np.random.exponential(lam)  
                    '''
                    people.append([arrival_interval,service_time])
                    event_list.append([len(arrival_list)+1,'arrivals',clock+arrival_interval])
                    departures_time_list.append(people[len(arrival_list)][1])              
                else:
                    departures_list.append(move)
                    server -= 1
                    served_system_time += clock-serving_people[-1]
                    served_queue_time +=  clock-serving_people[-1] -people[move[0]-1][-1]
                    queue_list.append(serving_people)
                    if len(temp_queue_list) > 0 and [move[0]]+['severed'] in severed_list:
                        queue -= 1
                        server += 1
                        severed_list.append([move[0]+1,'severed']) # arrange to severed list
                        serving_people = temp_queue_list[0]
                        #served_queue_time += clock - serving_people[-1] 
                        
                        del temp_queue_list[0]                    
                        event_list.append([move[0]+1,'departures',departures_time_list [0]+clock])
                        del departures_time_list [0]  
                        
                history_list.append([server]+move+[queue])
                del event_list[0]
                if len(history_list) > 1:
                    queue_square += history_list[state-1][-1]*(history_list[state][-2]-history_list[state-1][-2])
                    system_square += (history_list[state-1][-1]+history_list[state-1][0])*(history_list[state][-2]-history_list[state-1][-2])
                    if history_list[state-1][-1]+history_list[state-1][0] > 0:
                        NoIdle_time += history_list[state][-2]-history_list[state-1][-2]
                state += 1
                #--------------
                #if clock >warm_up_time:
                time.append(clock)
                L.append(system_square/clock)
                Lq.append(queue_square/clock)
                if len(departures_list) != 0:
                    W.append(served_system_time/len(departures_list))
                else:
                    W.append(0)
                if len(queue_list) != 0:
                    Wq.append(served_queue_time/len(queue_list))
                else:
                    Wq.append(0)     
                Idl.append(1-NoIdle_time/operating_time)
            
            service_seed += 2
            arival_seed += 2             
    
        if history_list[-1][-1]+history_list[state-1][0] > 0:
            NoIdle_time += operating_time - history_list[-1][-2]
        system_square += (history_list[-1][0]+history_list[-1][-1])*(operating_time-history_list[-1][-2])
        queue_square += history_list[-1][-1]*(operating_time-history_list[-1][-2])
      
        five_list[0].append(system_square/operating_time)
        five_list[1].append(queue_square/operating_time) 
        five_list[2].append(served_system_time/len(departures_list)) 
        five_list[3].append(served_queue_time/len(queue_list)) 
        five_list[4].append(1-NoIdle_time/operating_time)   
        
    plt.plot(time, L, 'bo', time, Lq, 'ko')
    plt.axhline(y=lamda/(mu-lamda), lw ='5',color='r')
    plt.axhline(y=lamda**2/mu/(mu-lamda), lw ='5',color='g')
    plt.show()
    plt.plot(time, W, 'bo', time, Wq, 'ko')
    plt.axhline(y=1/(mu-lamda)*60, lw ='5',color='r')
    plt.axhline(y=P/(mu-lamda)*60, lw ='5',color='g')
    plt.show()
    
    #plt.plot(time, Idl, 'bo')
    #plt.axhline(y=1-P, lw ='5',color='r')
    #plt.show()
        #print np.array(history_list) 
        #print 
     
    simulation = [system_square/operating_time,queue_square/operating_time,served_system_time/len(departures_list),served_queue_time/len(queue_list),1-NoIdle_time/operating_time]
    '''
    print '(a) Average number of customers in the system:',system_square/operating_time
    print '(b) Average number of customers in the queue:',queue_square/operating_time
    print '(c) Average time in the system:',served_system_time/len(departures_list)
    print '(d) Average time in the queue:',served_queue_time/len(queue_list)
    print '(e) Proportion of time the server is idle:',1-NoIdle_time/operating_time
    '''
    awef = ["Average number of customers in the system:","Average number of customers in the queue:","Average time in the system:","Average time in the queue:","Proportion of time the server is idle:"] 
    
    
    #print stats.t.ppf(1-0.025, 5)
    
    mean = [np.mean(five_list[i]) for i in range(5)]
    std = [np.std(five_list[i]) for i in range(5)]
    SE = [i/np.sqrt(n) for i in std]
    df = n-1
    Confidence_interval = []
    
    t_val = 1-(alpha)/2
    print
    for i in range(5):
        #print mean[i]-stats.t.ppf(t_val,df)*SE[i],"< Population mean < ",mean[i]+stats.t.ppf(t_val,df)*SE[i]
        Confidence_interval.append(stats.t.interval(t_val, df,loc = mean[i], scale = SE[i]))
        
        #x = np.linspace(t.ppf(0.01, df,mean[i],var[i]),t.ppf(0.99, df,mean[i],var[i]), 100)
        #fig, ax = plt.subplots(1, 1)
        #ax.plot(x, t.pdf(x, df,mean[i],var[i]),'r-', lw=5, alpha=0.6, label='t pdf')
    print
    print "------------------------Number of Repetitions:",n,"------------------------"
    print "------------------------Confidence Level:",(1-alpha)*100,"%---------------------------"
    
    print
    ModelTable = pd.DataFrame(
        {   "" :awef,
            "Model": ["L","Lq","W","Wq","Idl"],
            "Formulation": formulation,
            "TrialMean": mean,
            "LastSimulation": simulation,
            "Confidence interval": Confidence_interval
        }
    )
    display(ModelTable[["","Model","Formulation","TrialMean","LastSimulation","Confidence interval"]])
    '''
    for i in range(5):
        five_list[i] = sorted(five_list[i])
        fit = stats.norm.pdf(five_list[i], mean[i], std[i])  #this is a fitting indeed
        plt.plot(five_list[i],fit,'r-',lw ='5')
        plt.hist(five_list[i],color='b',normed=True)      #use this to draw histogram of your data
        plt.show() 
    '''
    return time,L,W,Lq,Wq,formulation