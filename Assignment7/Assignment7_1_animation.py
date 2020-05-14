# -*- coding: utf-8 -*-
"""
Created on Tue May 08 14:21:11 2018

@author: Yang
"""
from Tkinter import *
import math
import numpy as np
import random
import copy
import networkx as nx


door_coordinate = (1,1)
remain_probability = 0
#people_movement.txt
action_key = []
outfile = open('people_movement1.txt','r')
for row in outfile:
    word = row.split(' ')
    del word[-1]
    xy = []
    for j in range(len(word)/2):
        #print j
        xy.append([int(word[j*2]),int(word[j*2+1])])
    action_key.append(xy)
    #outfile.write(str(row) + ',' +'\n')
outfile.close()

people_number = len(action_key[0])


#for i in action_key:
    #print i
# transfer i,j into x,y and build floor and  obstacle
import csv
maze = []
with open('maze1.csv','rb') as csv_file:
    rows = csv.reader(csv_file)
    for row in rows:
        maze.append(row)

        print(', '.join(row))
    
obstacle_field = {}
  
maze_shape = np.array(maze)
floor_size =maze_shape.shape
for i in range(maze_shape.shape[0]):
    for j in range(maze_shape.shape[1]):
        if maze[i][j] == '0':
            obstacle_field[(j,maze_shape.shape[0]-1-i)] = 0
        else:
            obstacle_field[(j,maze_shape.shape[0]-1-i)] = 1

x_range = 30
canvas_height = (floor_size[0])*x_range
canvas_width = (floor_size[1])*x_range
 
x_origin = floor_size[1]
y_origin = floor_size[0]

xy_shift = 0.5
time = canvas_width/x_range

def physical2canvas(action_key):
    
    for move in action_key:
        for i in range(len(move)): 
            move[i] = ((move[i][0]+xy_shift)*x_range,canvas_height-(move[i][1]+xy_shift)*x_range)
    return action_key


new_move_dict = physical2canvas(action_key)
new_cell_initial_coordinate = new_move_dict[0]



root = Tk()
c = Canvas(root,width=canvas_width, height=canvas_height)
c.pack()
#draw the obstacle
for key, value in obstacle_field.iteritems():
    if value == 0:
        a = key[0]
        b = key[1]
        a = (a+xy_shift)*x_range
        b = canvas_height - (b+xy_shift)*x_range
        c.create_rectangle(a-x_range/2,b-x_range/2,a+x_range/2,b+x_range/2.0,fill="black")
'''
c.create_rectangle(0,0,x_range,canvas_width,fill="black")  
c.create_rectangle(0,0,canvas_width,x_range,fill="black") 
c.create_rectangle(canvas_width-x_range,0,canvas_width,canvas_width,fill="black")
c.create_rectangle(0,canvas_width-x_range,canvas_width,canvas_width,fill="black")

for i in range(1,time+2):
    c.create_line(i*x_range,0, i*x_range,(time)*x_range)
    c.create_line(0,i*x_range,(time)*x_range, i*x_range)
'''
text_2_id=c.create_text((door_coordinate[0]+xy_shift)*x_range, canvas_height-(door_coordinate[1]+xy_shift)*x_range, text='*')

c.update()
c.after(1000)

for i in range(people_number):
    locals()['oval_%s' % (i)] = c.create_oval(new_cell_initial_coordinate[i][0]-x_range/2, new_cell_initial_coordinate[i][1]-x_range/2, (new_cell_initial_coordinate[i][0]+1)+x_range/2, (new_cell_initial_coordinate[i][1])+x_range/2, fill='red', outline='blue')
    locals()['text_%s' % (i+1)] = c.create_text(new_cell_initial_coordinate[i][0], (new_cell_initial_coordinate[i][1]),text='%s'%(i))
c.update()
c.after(1000)
for new_move_position in np.array(new_move_dict):
    for i in range(people_number):
        c.coords(locals()['oval_%s' % (i)],new_move_position[i][0]-x_range/2, new_move_position[i][1]-x_range/2,new_move_position[i][0]+x_range/2,new_move_position[i][1]+x_range/2)
        c.coords(locals()['text_%s' % (i+1)],new_move_position[i][0], new_move_position[i][1])
    c.update()
    c.after(200)
c.mainloop()  




















