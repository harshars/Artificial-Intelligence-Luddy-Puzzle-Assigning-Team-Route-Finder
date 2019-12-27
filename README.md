# Part 1: The Luddy puzzle

Here are three variants of the 15-puzzle that we studied in class:

1. Original: This is the original puzzle. The game board consists of a 4x4 grid with 15 tiles numbered from 1 to 15. In each turn, the player can slide a tile into an adjacent empty space. Here are two sample moves of this puzzle:

2. Circular: In this variant, all of the moves of the original game are allowed but if the empty space is on the edge of the board, the tile on the opposite side of the board can be moved into the empty space (i.e., it slides off the board and “wraps around” to the other side). If an empty space is on a corner, then two possible “circular” moves are possible.

3. Luddy: This variant honors our school’s building’s namesake because all moves are in the shape of a letter “L”. Specifically, the empty square may be filled with the tile that is two positions to the left or right and one position up or down, or two positions up or down and one position left or right.

The goal of the puzzle is to find the shortest sequence of moves that restores the canonical configuration (on the left above) given an initial board configuration. We’ve written an initial implementation of a program to solve these puzzles — find it in your github repository. You can run the program like this:

```
./solve_luddy.py [input-board-filename] [variant]
where input-board-filename is a text file containing a board configuration in a format like:
5 7 8 1
10 2 4 3
6 9 11 12 
15 13 14 0
```
where 0 indicates the empty tile, and variant is one of original, circular, or luddy. We’ve included a few sample test boards in your repository. While the program works, the problem is that it is quite slow for complicated boards. Using this code as a starting point, implement a faster version, using A* search with a suitable heuristic function that guarantees finding a solution in is few moves as possible.

The program can output whatever you’d like, except that the last line of output should be a machine-readable representation of the solution path you found, in this format:

[move-1][move-2]...[move-n]
where each move is encoded as a letter, indicating the direction that a tile should be moved. For Original and Circular, the possible moves are L, R, U, or D for left, right, up, or down, respectively, indicating the direction that a tile should be moved.

For Luddy, the possible moves should be indicated with letters as follows: A for moving up two and left one, B for moving up two and right one, C for moving down two and left one, D for moving down two and right one, E for moving left two and up one, F for moving right two and up one, G for moving left two and down one, and H for moving right two and down one

## Solution

First we check if the solution exists for the board by calculating permutation inversion. If the solution exists then do the following:

### Algorithm

```
1. If GOAL?(initial-state) then return initial-state
2. INSERT(initial-node, FRINGE)
3. Repeat:
4.   If empty(FRINGE) then return failure
5.   s = REMOVE(FRINGE)
6.   INSERT(s, CLOSED)
7.   If GOAL?(s) then return s and/or path
8.   For every state s’ in SUCC(s):
9.      If s’ in CLOSED, discard s’
10.     If s’ in FRINGE with larger s’, remove from FRINGE
11.     If s’ not in FRINGE, INSERT(s’, FRINGE)

```

```
States: Any arrangement of numbers from 0 to 15

Initial state S0: Given input

Successor function: Given by available actions (sliding "0") L, R, U, D for Original and Circular, A, B, C, D, E, F, G, H for Luddy to move closer to the goal state

Goal state: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]

Cost function: For Original and Circular A* = g(s) + h(s), where g(s) is the cost and h(s) is Manhattan heuristic function. For Luddy g(s) is the cost and h(s) is Number of misplaced tiles heuristic function. Havent used Manhattan heuristic function for luddy because it is not admissable. Also tried to use luddy distance i.e number of L shaped moves required to reach its final position by restricting the depth to 2 (Kind of Iterative deepening search for the heuristic)

```
**Sample Output**

```
Start state: 
  1   2   3   4
  5   0   6   7
  9  10  11   8
 13  14  15  12
Solving...
Solution found in 4 moves:
LLUU
```

# Road trip!

Besides baseball, McDonald’s, and reality TV, few things are as canonically American as hopping in the car for an old-fashioned road trip. We’ve prepared a dataset of major highway segments of the United States (and parts of southern Canada and northern Mexico), including highway names, distances, and speed limits; you can visualize this as a graph with nodes as towns and highway segments as edges. We’ve also prepared a dataset of cities and towns with corresponding latitude-longitude positions. These files should be in the GitHub repo you cloned in step 0. Your job is to implement algorithms that find good driving directions between pairs of cities given by the user. Your program should be run on the command line like this:

```
./route.py [start-city] [end-city] [cost-function]
where:
• start-city and end-city are the cities we need a route between. 
• cost-function is one of:
  – segments tries to find a route with the fewest number of “turns” (i.e. edges of the graph)
  – distance tries to find a route with the shortest total distance
  – time tries to find the fastest route, for a car that always travels at the speed limit
  – mpg tries to find the most economical route, for a car that always travels at the speed limit and
  whose mileage per gallon (MPG) is a function of its velocity (in miles per hour), as follows:
  MPG(v)=400*v/150*(1− v/150)^4

```

The output of your program should be a nicely-formatted, human-readable list of directions, including travel times, distances, intermediate cities, and highway names, similar to what Google Maps or another site might produce. In addition, the last line of output should have the following machine-readable output about the route your code found:
[total-segments] [total-miles] [total-hours] [total-gas-gallons] [start-city] [city-1] [city-2] ... [end-city]

## Solution

We wanted to use Lattitude and Longitude as the heuristic function for the distance optimization, but there were missing co-ordinates, taking the median for the missing co-ordinates didnt give us the right answer. Hence we did not go with A* search for this problem. We just used Heapq to optimize based on the input given.

### Algorithm

```
1. If GOAL?(initial-state) then return initial-state
2. INSERT(initial-node, FRINGE)
3. INSERT(initial-node, VISITED)
4. Repeat:
5.  If empty(FRINGE) then return failure
6.    s = REMOVE(FRINGE)
7.    If GOAL?(s) then return s and/or path
8.    For every state s’ in SUCC(s):
9.      INSERT(s’, FRINGE)
10.     INSERT(s', Visited)

```

```
States: Any arrangement of numbers from 0 to 15

Initial state S0: Given Start city

Successor function: Cities connected to the next city based on the cost function provided (distance, mpg, time or segments)

Goal state: Given End city

Cost function: Distance, mpg, time or segments

```

**Sample Output**

```
./route.py Indianapolis,_Indiana Bloomington,_Indiana mpg
3 51 1.079500 1.955200 Indianapolis,_Indiana Jct_I-465_&_IN_37_S,_Indiana Martinsville,_Indiana Bloomington,_Indiana
```

# Part 3: Choosing a team

In the dystopian future, AI will have taken over most labor and leadership positions. As a student in B551, you will assemble teams of robots to do the assignments for you. SICE will have a set of available robots for you to choose from. Each robot i will have an hourly rate Pi and a skill level Si. You’ll want to choose a team of robots that has the greatest possible skill (i.e., the sum of the skill levels is as high as possible), but you have a fixed budget of just B Intergalactic EuroYuanDollars (EYDs).

```
The robot names, skills, and rates will be given in a file format like this:
David 34 100.5
Sam 25 30
Ed 12 50
Glenda 50 101
Nora 1 5
Edna 45 80
```

## Solution

Methods tried:

  -> 0/1 knapsack problem using dynammic programming. This was not considered because of the integer value being used.
  
  -> Tried Heapq search implementation which tries to find every combination of the robots given. Since there is no pruning its very slow and works well for smaller inputs
  
  -> Branch and Bound 0/1 Knapsack Algorithm 

Branch and Bound 0/1 Knapsack Algorithm was the fastest which prunes the tree whenever it crosses the budgets. Detailed description is mentioned below.

Citation: https://www.geeksforgeeks.org/0-1-knapsack-using-branch-and-bound/

### Algorithm

```
  1. Sort all items in decreasing order of ratio of skills per unit cost so that an upper bound can be computed using Greedy       Approach.
  2. Initialize maximum skills, maxSkills = 0
  3. Create an empty queue, Q.
  4. Create a dummy node of decision tree and enqueue it to Q. Skills and cost of dummy node are 0.
  5. Do following while Q is not empty.
     Extract an item from Q. Let the extracted item be u.
     Compute skills of next level node. If the skills is more than maxSkills, then update maxSkills.
     Compute bound of next level node. If bound is more than maxSkills, then add next level node to Q.
     Consider the case when next level node is not considered as part of solution and add a node to queue with level as next,      but cost and Skills without considering next level nodes.
```

```
States: Every combination of considering the robot or not considering the robot.

Initial state S0: Dummy Node with no robots selected.

Successor function: Considering the subsequent robot.

Goal state: The optimum skills of robots given the cost.

Cost function: Computing the upper bound and cost of the next level nodes. Upper bound is total skills till the current level node. Cost is the total skills as per greedy approach.

Pruning methods used:
    If the cost of the next level node exceeds the budget then the next level node will not be considered. 
    If the cost [total skills till the next level node plus the skills calculated for the fractional cost from the remaining budget]
    
```
   
**Sample Output**

For above mentioned input with budget as 100

```
Found a group with 2 people costing 85.000000 with total skill 46.000000
Edna 1.000000
Nora 1.000000
```


