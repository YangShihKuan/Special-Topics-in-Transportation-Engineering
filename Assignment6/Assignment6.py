# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 21:23:54 2018

@author: Yang
"""

from Tkinter import *
import math
import numpy as np
import random
import copy
people_number = 3
floor_size = 11
door_coordinate = (11,3)
remain_probability = 0.2
#--------------------------------------
'''
root = Tk()
c = Canvas(root,width=(floor_size+1)*40, height=(floor_size+1)*40)
c.pack()

for i in range(1,floor_size+2):
    c.create_line(i*40,0, i*40,(floor_size+1)*40)
    c.create_line(0,i*40,(floor_size+1)*40, i*40)
text_2_id=c.create_text(door_coordinate[0]*40+20, door_coordinate[1]*40+20, text='11,3')

#c.update()
#--------------------------------------
'''
floor_key = [(i+1,j+1) for i in range(floor_size) for j in range(floor_size) ]
floor_value = [ -math.sqrt((i-door_coordinate[0])**2+(j-door_coordinate[1])**2) for i in range(floor_size) for j in range(floor_size)]

people_key = [i for i in range(people_number)]
people_initial_coordinate = []
while len(people_initial_coordinate) < people_number:
    chosen_one = random.choice(floor_key)
    if chosen_one not in people_initial_coordinate:
        people_initial_coordinate.append(chosen_one)
#print people_initial_coordinate
static_field = dict(zip(floor_key,floor_value))
occupied_field = dict(zip(floor_key,[0]*floor_size**2))
obstacle_field = dict(zip(floor_key,[1]*floor_size**2))

for i in people_initial_coordinate:
    occupied_field[i] = 1

cell_position = dict(zip(people_key,people_initial_coordinate))
cell_target = dict(zip(people_key,people_initial_coordinate))
'''
for i in range(people_number):
    locals()['oval_%s' % (i)] = c.create_oval(cell_position[i][0]*40, cell_position[i][1]*40, (cell_position[i][0]+1)*40, (cell_position[i][1]+1)*40, fill='red', outline='blue')
    locals()['text_%s' % (i)] = c.create_text(cell_position[i][0]*40 +20, (cell_position[i][1]*40) +20,text='%s'%(i))
    c.update()
'''
asd = False
cell_initial_coordinate = dict(zip(people_key,people_initial_coordinate))
move_dict = [cell_initial_coordinate]








for move in range(30): 
    #print "-------",move+1,'-------'
    for i in people_key:
        #adjacent_cell = cell_position[i]
        xy_exp_sum = 0
        xy_exp_list = []
        candidate_position = []
        for x in [cell_position[i][0]-1,cell_position[i][0],cell_position[i][0]+1]:
            for y in [cell_position[i][1]-1,cell_position[i][1],cell_position[i][1]+1]:
                
                if (x,y) in floor_key:
                    candidate_position.append((x,y))
                    xy_exp = math.exp(static_field[x,y])*(1-occupied_field[x,y])*obstacle_field[x,y]
                    

                    #occupied_field[x,y] = 0
                    
                    xy_exp_sum += xy_exp
                    xy_exp_list.append(xy_exp)
    
        candidate_probability = [j/xy_exp_sum for j in xy_exp_list]
        cell_target[i] = candidate_position[np.random.choice(len(candidate_position),p = candidate_probability)]
    
        #print np.array(candidate_position)
        #print np.array(candidate_probability)
        
    #print cell_target
    conflict_key = []
    conflict_field = {}    
    for key, value in cell_target.iteritems():
       if value not in conflict_field:
           conflict_field[value] = [key]
       else:
           conflict_field[value].append(key)   
    #print conflict_field    
    #conflict_field = {(2, 5): [0,3], (1, 10): [1], (7, 7): [2]}   
    for key, value in conflict_field.iteritems():
        
        if len(value) > 1:
            
            #print "------------------"
            #print conflict_field
            #print value
            move_probability = np.random.uniform(0,1)
            #print move_probability
            if move_probability <= remain_probability:
                for i in value:
                    cell_target[i] = cell_position[i]
            else:
                remain_one = random.sample(value,len(value)-1)
                #print "remain",remain_one
                for i in remain_one:
                    cell_target[i] = cell_position[i]
    #print cell_target
    #print cell_position
    for key, value in cell_target.iteritems():
        if cell_position[key] != value:
            occupied_field[cell_position[key]] = 0 
            cell_position[key] = value
            occupied_field[value] = 1
        #cell_position[key] = value
    copy_cell_position = copy.copy(cell_position)
    #print "cell_position",cell_position
    #print "copy_cell_position",copy_cell_position
    move_dict.append(copy_cell_position)
    #print "********",cell_position
    ''''
    for key, value in cell_position.iteritems():

        occupied_field[value] = 1
    '''
    #print cell_position
    #print conflict_field 
    '''
    for i in range(people_number):
        c.coords(locals()['oval_%s' % (i)],cell_position[i][0]*40, cell_position[i][1]*40, (cell_position[i][0]+1)*40, (cell_position[i][1]+1)*40)
        c.coords(locals()['text_%s' % (i)],cell_position[i][0]*40 +20, (cell_position[i][1]*40) +20)
        #locals()['oval_%s' % (i)] = c.create_oval(cell_position[i][0]*40, (cell_position[i][1]-1)*40, (cell_position[i][0]+1)*40, cell_position[i][1]*40, fill='red', outline='blue')    
    c.update()
    c.after(2000)
    '''
for move_position in np.array(move_dict):
    print move_position

    
'''
    
root = Tk()
c = Canvas(root,width=(floor_size+1)*40, height=(floor_size+1)*40)
c.pack()

for i in range(1,floor_size+2):
    c.create_line(i*40,0, i*40,(floor_size+1)*40)
    c.create_line(0,i*40,(floor_size+1)*40, i*40)
text_2_id=c.create_text(door_coordinate[0]*40+20, door_coordinate[1]*40+20, text='11,3')

for i in range(people_number):
    locals()['oval_%s' % (i)] = c.create_oval(cell_position[i][0]*40, cell_position[i][1]*40, (cell_position[i][0]+1)*40, (cell_position[i][1]+1)*40, fill='red', outline='blue')
    locals()['text_%s' % (i)] = c.create_text(cell_position[i][0]*40 +20, (cell_position[i][1]*40) +20,text='%s'%(i))
    c.update()

for move_position in np.array(move_dict):
    for i in range(people_number):
        c.coords(locals()['oval_%s' % (i)],move_position[i][0]*40, move_position[i][1]*40, (move_position[i][0]+1)*40, (move_position[i][1]+1)*40)
        c.coords(locals()['text_%s' % (i)],move_position[i][0]*40 +20, (move_position[i][1]*40) +20)
        #locals()['oval_%s' % (i)] = c.create_oval(cell_position[i][0]*40, (cell_position[i][1]-1)*40, (cell_position[i][0]+1)*40, cell_position[i][1]*40, fill='red', outline='blue')    
    c.update()
    c.after(2000)    
    #c.update()
#--------------------------------------
    '''