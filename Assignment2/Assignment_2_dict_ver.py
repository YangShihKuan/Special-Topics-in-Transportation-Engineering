import copy
import networkx as nx

node_number=[x for x in range(1,8)]
path = [(1,2,2.0),(1,4,4.0),(2,3,2.0),(3,5,1.0),(3,6,3.0),(4,2,1.0),(4,5,3.0),(4,7,1.0),(5,6,1.0)]


scenarios = [
[1,1,1,1,1,1,1,0,	1],
[0,1,0,1,0,1,1,1,	1],
[1,1,1,0,1,0,1,1,	1],
[1,0,1,1,1,1,0,0,	0],
[0,0,0,0,0,0,0,0,	0]
]

demand = [2.0,1.0,1.0,2.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,2.0,1.0,1.0]

G = nx.DiGraph()
for a in node_number:
    G.add_node(a)
for i in path:
    G.add_weighted_edges_from([i])

OD_list = []
short_t = []

for i in node_number:
    for j in node_number:
        if nx.has_path(G, i, j) == True and i != j:
            OD_list.append((i,j))
            short_t.append(nx.dijkstra_path_length(G, source=i, target=j))
            
OD_short_list = dict(zip(OD_list,short_t))
OD_demand_list = dict(zip(OD_list,demand))

number = len(path)
budget = 4  #maximum number of facilities
 
from pyevolve import G1DBinaryString
from pyevolve import GSimpleGA
from pyevolve import Selectors
from pyevolve import Mutators


def eval_func(chromosome):
    directness = 0.0
    protect_scenarios = copy.deepcopy(scenarios)
    for i in range(len(scenarios)):
            
        protect_path = []
        for j in range(len(protect_scenarios[i])):
            if chromosome[j] == 1:
                protect_scenarios[i][j] = 1
            if protect_scenarios[i][j] == 1:
                protect_path.append(path[j])
    
        H = nx.DiGraph()
        for a in node_number:
            H.add_node(a)
        for a in protect_path:
            H.add_weighted_edges_from([a])        

        free_flow = copy.deepcopy(OD_short_list)
        for a,b in OD_list:
            if nx.has_path(H, a, b) == True:
                free_flow[(a,b)] = nx.dijkstra_path_length(H, source=a, target=b)
            elif nx.has_path(H, a, b) == False:
                free_flow[(a,b)] = -1

        counter = [OD_demand_list[(a,b)]*OD_short_list[(a,b)]/free_flow[(a,b)] for a,b in OD_list if free_flow[(a,b)] != -1]

        directness += 0.2*sum(counter)

    if sum(chromosome) > budget:
         directness = directness - 2*sum(chromosome)  
       
    return directness
    
def run_main():
   # Genome instance
   genome = G1DBinaryString.G1DBinaryString(9)

   # The evaluator function (objective function)
   genome.evaluator.set(eval_func)
   genome.mutator.set(Mutators.G1DBinaryStringMutatorFlip)

   # Genetic Algorithm Instance
   ga = GSimpleGA.GSimpleGA(genome)
   ga.selector.set(Selectors.GTournamentSelector)
   ga.setGenerations(100)

   # Do the evolution, with stats dump
   # frequency of 10 generations
   ga.evolve(freq_stats=20)

   # Best individual
   print (ga.bestIndividual())

if __name__ == "__main__":
   run_main()



