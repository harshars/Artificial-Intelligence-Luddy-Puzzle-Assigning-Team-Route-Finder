#!/usr/local/bin/python3
# solve_luddy.py : Sliding tile puzzle solver
#
# Code by: [Harsha Raja Shivakumar | Maithreyi Manur Narasimha Prabhu | Sunny Bhati]
#
# Based on skeleton code by D. Crandall, September 2019
#
import heapq
import sys
import time


MOVES = { "R": (0, -1), "L": (0, 1), "D": (-1, 0), "U": (1,0) }

# Check 

def find_luddy_distance_each(actual_position, number):
    row,column = ind2rowcol(number)
    fringe = set()
    #visited = set()
    #visited.add((row, column))
    fringe.add((row, column, 1))
    depth = 0

    while len(fringe) > 0 and depth <= 64:
        row, column, count = fringe.pop()
        for i in list(MOVES.items()):
            row1 = row + i[1][0]
            column1 = column + i[1][1]
            if rowcol2ind(row1, column1)==actual_position:
                return count
            else:
                #if (row1, column1) not in visited:
                fringe.add((row1,column1, count+1))
                depth = depth + 1

    return 3


def luddy_distance(board):
    #temp = [1, 2, 3, 4 ,5 ,6 ,7,8, 9, 10, 11,12,13,14,15,0]
    count = 0
    for i in range(len(board)):
        if(board[i] != i+1) and board[i]!=0:
            count += find_luddy_distance_each(i+1, board[i])

    return count

# Used the onlien code for calculating this
def manhattan_distance(board):
    return sum(abs((val-1)%4 - i%4) + abs((val-1)//4 - i//4) for i, val in enumerate(board) if val)

def misplaced(board):
    #temp = [1, 2, 3, 4 ,5 ,6 ,7,8, 9, 10, 11,12,13,14,15,0]
    count = 0
    for i in range(len(board)):
        if(board[i] != i+1):
            count += 1
    return count

def rowcol2ind(row, col):
    return row*4 + col

def ind2rowcol(ind):
    return (int(ind/4), ind % 4)

def valid_index(row, col):
    return 0 <= row <= 3 and 0 <= col <= 3

def swap_ind(list, ind1, ind2):
    return list[0:ind1] + (list[ind2],) + list[ind1+1:ind2] + (list[ind1],) + list[ind2+1:]

def swap_tiles(state, row1, col1, row2, col2):
    return swap_ind(state, *(sorted((rowcol2ind(row1,col1), rowcol2ind(row2,col2)))))

def printable_board(row):
    return [ '%3d %3d %3d %3d'  % (row[j:(j+4)]) for j in range(0, 16, 4) ]

# return a list of possible successor states
def successors(state, cost, cost_final):
    (empty_row, empty_col) = ind2rowcol(state.index(0))
    return [ (cost, cost_final, swap_tiles(state, empty_row, empty_col, empty_row+i, empty_col+j), c) \
             for (c, (i, j)) in MOVES.items() if valid_index(empty_row+i, empty_col+j) ]

# check if we've reached the goal
def is_goal(state):
    return sorted(state[:-1]) == list(state[:-1]) and state[-1]==0
    
def solve(initial_board, type):
    timeout = time.time() + 60*3
    heap = []
    visited = set()
    visited.add(initial_board)
    heapq.heappush(heap, (0, 0, initial_board, ""))
    while len(heap) > 0:
        (cost, cost_final, state, route_so_far) = heapq.heappop(heap)
        for (cost, cost_final, succ, move) in successors( state, cost, cost_final):
            if is_goal(succ):
                return( (cost_final+1,route_so_far + move) )
            
            if succ not in visited:
                if type!="luddy":
                    heapq.heappush(heap, (cost+1+manhattan_distance(succ), cost_final+1, succ, route_so_far + move))
                else:
                    heapq.heappush(heap, (cost+1+misplaced(succ), cost_final+1, succ, route_so_far + move))
                visited.add(succ)

        if time.time() > timeout:
            return 1
        
    return False

def solve1(initial_board, type):
    heap = []
    visited = set()
    visited.add(initial_board)
    heapq.heappush(heap, (0, 0, initial_board, ""))
    while len(heap) > 0:
        (cost, cost_final, state, route_so_far) = heapq.heappop(heap)
        for (cost, cost_final, succ, move) in successors( state, cost, cost_final):
            if is_goal(succ):
                return( (cost_final+1,route_so_far + move) )
            
            if succ not in visited:
                if type!="luddy":
                    heapq.heappush(heap, (cost+1+manhattan_distance(succ), cost_final+1, succ, route_so_far + move))
                else:
                    heapq.heappush(heap, (misplaced(succ), cost_final+1, succ, route_so_far + move))
                visited.add(succ)
        
    return False

def permutation_inversion_check(board):
    final_cost = 0
    for i in range(0, len(board)):
        if board[i]!=0:
            cost_temp = 0
            for j in range(i+1, len(board)):
                if (board[i] > board[j]) & (board[j] != 0):
                    cost_temp+= 1    
            final_cost+= cost_temp
    temp1 = [1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4]
    final_cost+=temp1[board.index(0)]

    return final_cost

# test cases
if __name__ == "__main__":
    if(len(sys.argv) != 3):
        raise(Exception("Error: expected 2 arguments"))

    start_state = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [ int(i) for i in line.split() ]

    if len(start_state) != 16:
        raise(Exception("Error: couldn't parse start state file"))

    if(sys.argv[2] == "circular"):
        MOVES.update({ "R1" : (0, -3)})
        MOVES.update({ "L1" : (0, 3)})
        MOVES.update({ "D1" : (-3, 0)})
        MOVES.update({ "U1" : (3,0)})

    if(sys.argv[2] == "luddy"):
        MOVES = {}
        MOVES.update({ "E" : (-2, -1)})
        MOVES.update({ "F" : (-2, 1)})
        MOVES.update({ "G" : (2, -1)})
        MOVES.update({ "H" : (2, 1)})
        MOVES.update({ "A" : (-1, -2)})
        MOVES.update({ "B" : (-1, 2)})
        MOVES.update({ "C" : (1, -2)})
        MOVES.update({ "D" : (1, 2)})

    print("Start state: \n" +"\n".join(printable_board(tuple(start_state))))

    print("Solving...")

    #tic = time.time()

    if permutation_inversion_check(start_state)%2==0:
        route = solve(tuple(start_state), sys.argv[2])
        if route==1:
            route = solve1(tuple(start_state), sys.argv[2])
        final_path = str(route[1])
        final_path = final_path.replace("R1", "R")
        final_path = final_path.replace("L1", "L")
        final_path = final_path.replace("U1", "U")
        final_path = final_path.replace("D1", "D")
        
        print("Solution found in " + str(route[0]) + " moves:" + "\n" + final_path)
    else:
        print("Inf")

    #toc = time.time()
    #print(toc-tic)

