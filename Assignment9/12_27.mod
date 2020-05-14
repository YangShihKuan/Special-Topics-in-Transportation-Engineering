set All;
set Node;
set Node_1;
set Node_16;
set Car;


param deadline;
param time{i in All, j in All};
param n; #21
param one;
param two;

var x{i in All, j in All,k in Car}binary;
var van{k in Car}binary;
var u{i in All,c in Car} >= 0;

minimize total_cost: sum{k in Car,j in Node_1:j!=1}x[1,j,k];

subject to customer_assigned_one_route{i in Node}:sum{k in Car}sum{j in Node_16:i!=j}x[i,j,k] = one;

subject to form_depot{k in Car}:sum{j in Node_16}x[1,j,k]=one;
subject to back_depot{k in Car}:sum{i in Node_1}x[i,16,k]=one;

subject to in_and_out1{j in Node,k in Car}: sum{i in Node_1:i!=j} x[i,j,k] 
											= sum{i in Node_16:i!=j}x[j,i,k];


subject to time_limit{k in Car}:sum{i in All,j in Node_1:i!=j}time[i,j]*x[i,j,k] <= deadline;

#subject to leave_car{k in Car}:sum{j in Node_1:j!=1}x[1,j,k] <= van[k];

subject to subtours1{k in Car}:  u[1,k] = one;
subject to subtours2{k in Car,i in Node_16}:  two <= u[i,k] <= n;
subject to subtours3{k in Car,i in Node_16,j in Node_16:i!=j}:  u[i,k]-u[j,k] + one <= (one-x[i,j,k])*(n-one) ;


