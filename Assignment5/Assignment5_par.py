# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 00:05:47 2018

@author: user
"""

import MM1_trial as MM1_trial

#parameter_number = 3
operating_time = 1500
lam = 3.0 #service_time
scale = 6.0 #arrival_interval
n = 300
alpha = 0.05
arival_seed = 0
service_seed = 11

time,L,W,Lq,Wq,formulation= MM1_trial.MM1_trial(operating_time,lam,scale,n,alpha,arival_seed,service_seed)
