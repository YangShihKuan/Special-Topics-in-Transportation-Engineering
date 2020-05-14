## Assignment 1
1. Solve the furniture company problem in AMPL.
2. Read the section of "model formulation" in Chu and Chen (2016).

## Assignment 2 (Network protection considering reliability) 
1. Use the model formulation in Chu, J. C.* and Chen, S.-C. (2016) Optimization of Transportation Infrastructure System Protection Considering Weighted Connectivity Reliability, ASCE Journal of Infrastructure Systems, 22(1)  
2. Use the example in Chapter 3.2 of the master thesis by 陳仕棋. Note that there are typos in Table 3.2.1.  
3. Solve the problem using (1) a deterministic equivalent model and (2) the hybrid approach (Pyevolve for stage 1 and networkx for calculating directness in stage 2).


## Assignment 3 (system time-to-failure)
Build the simulation model for the system time-to-failure problem.  


## Assignment 4 (Performance measures)
1. System time-to-failure: Calculate performance measures  
(1) Time to failure  
(2) Average number of functional components  

2. M/M/1 queue  
2-1. Build the simulation model with the interarrival times and service times FOR THE FIRST SIX CUSTOMERS in the example.  
2-2. Calculate performance measures  
(a) Average number of customers in the system  
(b) Average number of customers in the queue  
(c) Average time in the system  
(d) Average time in the queue  
(e) Proportion of time the server is idle  


## Assignment 5
1. Estimate the performance measures of the system TTF problem  
2. Do experiments for a M/M/1 queue and compare the estimation using simulation and the values from the formulas of queueing theory.   
2-1. Try different parameters of mean interarrival time and mean service time. For example, 3/6, 6/6, 6/5, 6/3  
2-2. The formulas can be found in most of Operations Research textbooks or the Internet.  
2-3. Remember to report number of repetitions and the confidence interval of estimation error.  

About the random number generation in Python:  
1. It is recommended to use numpy.random instead of Python built-in random  
2. If you need only a single stream of random numbers, just set the seed and start generating random numbers.  
3. If you need to use multiple streams of random numbers simultaneously, you need to create multiple random number generators with different seeds and generate random numbers using these generators.  
4. Look up the Internet for documents and examples

## Assignment 6 (FFCA core)
Implement a FFCA based on the algorithm in Chu (2009)  
Start with a single pedestrian (Steps 1 and 2)  
Then consider multiple pedestrians and conflicts (Step 3)  
Ignore Step 4 about dynamic field. That is, set its values to zero and do not update.  
Simulate the pedestrian movements in a simple geometry (no obstacle)  
The example should be very small so you can calculate the static field by hand.  

## Assignment 7 (FFCA)  
Improve your FFCA model to deal with complex geometry  
Step 0: Initialize the static field for complex geometry by discretizing space into a cell-based network (as in Asano et al., 2010) and find shortest distances from all cells to the destination cell with a shortest path algorithm (networkx in Python).  
Simulate the pedestrian movements in a complex geometry with animation (tkinter in Python)  
Separate simulation and animation!!!  
Save the result of simulation in a file and then generate animation using the saved result in the file.  
Data for a maze is provided for testing  

## Assignment 8 (Dynamic programming)

## Assignment 9 (VRP)    
MBMP 12.23 Milk collection    
MBMP 12.27 Lost baggage distribution     

## Assignment 10 (VRPTW heuristics)  
VRPTW algorithms in Solomon (1987)  
1. Saving heuristics  
2. Nearest Neighbor heuristics 

## Assignment 11 (VRPTW heuristics)
Insertion heuristics using approach/type 1. 

## Assignment 12 (dynamic VRP)
The final assignment is to develop a "local-update" solution algorithm (a set of routing rules) for the dynamic VRP. (Reoptimization is computationally intensive and difficult to develop so not recommended.)

The benchmarks of dynamic VRP can be found at http://becool.info.ucl.ac.be/resources/benchmarks-dynamic-and-stochastic-vehicle-routing-problem-time-windows. The 15 problems in class 1 will be used.

On 6/20, you should have a proposal for your algorithm. By 6/27, you should implement the algorithm and run it to solve the 15 problems in class 1 on a designated computer (for a fair comparison). The total distance, vehicle used, and computational time of the 15 problems in class 1 should be reported as the final result.  









