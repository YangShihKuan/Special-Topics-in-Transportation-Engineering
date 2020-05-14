## ex12.3 model 
set Link; #link e
set Group;
set Path{g in Group};
set Scenario;

param budget; #budget
param cost{e in Link}; #cost
param demand{g in Group};
 
param m; # a large positive value
param probability{s in Scenario}; #probability of scenario s
param short_tt{g in Group}; #shortest
param path_tt{g in Group,p in Path[g]}; #freeflow
param delta{g in Group,p in Path[g],e in Link}; # e on the path p of group g
param tolerance; #tolerance value
param xi{e in Link,s in Scenario}; #link e under disaster scenario s
param one; #1


var Directness{g in Group,s in Scenario} >= 0, <=1;
var Indicate{g in Group,p in Path[g],s in Scenario} binary; 
var Notserved{g in Group,s in Scenario} binary;
var Underprotected{e in Link} binary;
var X{e in Link,s in Scenario} binary; #link e functional
var Y{g in Group,p in Path[g],s in Scenario} binary; #path p connected

maximize directness: sum{s in Scenario} probability[s]*(sum{g in Group} demand[g]*Directness[g,s]) ;

subject to budget1 : sum{e in Link} cost[e]*Underprotected[e] <= budget;
subject to functional2{e in Link,s in Scenario}: Underprotected[e] + (one - Underprotected[e])*xi[e,s] = X[e,s];

subject to ensures3{g in Group,p in Path[g],s in Scenario}: sum{e in Link} delta[g,p,e] - sum{e in Link} delta[g,p,e]*X[e,s] <= m*(one-Y[g,p,s]);
subject to ensures4{g in Group,p in Path[g],s in Scenario}: sum{e in Link} delta[g,p,e] - sum{e in Link} delta[g,p,e]*X[e,s] >= tolerance - m*Y[g,p,s];

subject to directness7{g in Group,p in Path[g],s in Scenario}: Indicate[g,p,s] <= Y[g,p,s];
subject to directness8{g in Group,s in Scenario}: sum{p in Path[g]} Indicate[g,p,s] + Notserved[g,s] = one;
subject to directness9{g in Group,s in Scenario}: Directness[g,s] = sum{p in Path[g]} Indicate[g,p,s]*(short_tt[g]/path_tt[g,p]);
