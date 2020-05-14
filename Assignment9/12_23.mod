
set All;
set EDfarm;
set EODfarm;
set Day;



param collection{i in All};
param x_axle{i in All};
param y_axle{i in All};

param cost{i in All, j in All} = sqrt((x_axle[i]-x_axle[j])^2+(y_axle[i]-y_axle[j])^2);
param capacity;
param n; #21
param one;
param two;
param ten;
var x{i in All, j in All, d in Day} binary;
#var y{i in All,d in Day} binary;
var u{i in All,d in Day} >= 0;

minimize total_cost: sum{d in Day,i in All, j in All:i!=j } cost[i,j]*x[i,j,d]*ten ;

subject to in_and_out{j in All,d in Day}:sum{i in All:i!=j} x[i,j,d] = sum{i in All:i!=j}x[j,i,d];
subject to back_to_depot{d in Day}: sum{i in All:i!=1}x[i,1,d] = one;
subject to capacity_limit{d in Day}: sum{i in All} collection[i]*sum{j in All}x[i,j,d] <= capacity ;

#######################
subject to assign_EODfarm{i in EODfarm}: sum{d in Day,j in All:j!=i}x[i,j,d] = one;

#subject to assign_EODfarm2{i in EODfarm,d in Day}: sum{j in All:j>i}x[i,j,d] + sum{j in All:j<i}x[j,i,d] = two*y[i,d];
subject to assign_EDfarm{i in EDfarm,d in Day}: sum{j in All:j!=i}x[i,j,d]= one;



subject to subtours1{d in Day}:  u[1,d] = one;
subject to subtours2{d in Day,i in All:i !=1}:  two <= u[i,d] <= n;
subject to subtours3{d in Day,i in All,j in All:i !=1 and j !=1}:  u[i,d]-u[j,d] + one <= (one-x[i,j,d])*(n-one) ;


