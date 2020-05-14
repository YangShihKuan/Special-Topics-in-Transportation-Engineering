## ex12.3 model 

set Product;
set Scenario;
set Resource;

param P{s in Scenario}; 
param Price{p in Product};
param Cost{r in Resource}; 
param Demand{p in Product,s in Scenario}; 
param Required{p in Product,r in Resource}; 

var x{r in Resource} >= 0;
var y{p in Product,s in Scenario} >= 0; 


maximize profit: sum{r in Resource} -Cost[r]*x[r] + sum{p in Product,s in Scenario} P[s]*Price[p]*y[p,s] ;

subject to required_limit{r in Resource,s in Scenario}: sum{p in Product} Required[p,r]*y[p,s] <= x[r];
subject to scenario_limit{p in Product,s in Scenario}: y[p,s] <= Demand[p,s];

