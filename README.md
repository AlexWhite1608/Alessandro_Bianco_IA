# Introduction

This project is used to solve a map-colouring problem using a backtracking algorithm. 
The main goal is to compare the performance of the two inference algorithms: *Forward Checking* vs 
*Maintaining Arc Consistency*.

## Project structure

Below is the list of files that make up the project, divided into *src* and *testBT* which is the folder
that contains the test code for the algorithms:

- **Graph.py:** contains the source code for the structure of the graph, including the Node class and the methods used 
for the edge generation process.


- **Intersections.py:** in this file are contained all the functions needed to compute the intersection between the edges
of the graph. 


- **Backtracking.py:** source code for the backtracking algorithms implementation. 


- **Test.py:** contains the code for the test implementations. There are 3 different types of tests used to verify both 
the correct structure of the graph, using graphical visualization, and the performance of the two inference algorithms.


## Usages

In the **main.py** file we have three different functions called:

- **Test.test_graph_visualization(N_NODES, BT_TYPE)**: used to visualize the randomly generated graph with *N_NODES* number 
of nodes and *BT_TYPE* of backtracking algorithm applied. We can choose the number of the nodes of the graph simply by changing
the *N_NODES* constant parameter as well as changing the type of backtracking algorithm by setting *BT_TYPE* parameter to
the string *"ForwardChecking"* or *"Mac"*.


- **Test.time_comparison():** is used to compare the execution time of the two algorithms. We can change the domain size 
(the colors used for the assignment) by adding/deleting values from the *COLOR* parameter in the *Backtracking.py* file.


- **Test.test_failed_assignment():** this function is used to compare the number of failed assignments of the two algorithms
while incrementing the size of the graph. Also here we can change the domain size of each variable as well as in the previous
test performing the same action.