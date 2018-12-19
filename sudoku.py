import numpy as np
import random as r

def create_normal_sudoku_map():
    out = np.zeros((9,9),np.int8)
    inc = np.array([[1,1,1,2,2,2,3,3,3]])
    
    for i in [0,3,6]:
        big = np.concatenate((inc,inc,inc),axis=0)
        out[i:i+3,:] = big
        inc = np.add(inc,3)
    return out

def check_row_ava(number,row):
    if number in row:
        return False
    return True

def check_for_availability(sudoku,sudoku_map,number,coords):
    row_available = check_row_ava(number,sudoku[coords[0],:])
    column_available = check_row_ava(number,sudoku[:,coords[1]])
    
    colour = sudoku_map[coords]
    
    result = (lambda x: x == number)(sudoku)
    colours = (lambda x: x == colour)(sudoku_map)
    
    same_colour_same_number = np.multiply(result,colours)
    
    if(row_available and column_available and True not in same_colour_same_number):
        return True
    return False

def create_heuristic_random(sudoku_map,filled = 17):
    sudoku_heuristic = np.ones(sudoku_map.shape,np.int8)
    length = max(sudoku_map.shape)
    
    while filled >= 0:
        i = r.randint(0,length - 1)
        j = r.randint(0,length - 1)
        
        if sudoku_heuristic[i,j] != 2:
            sudoku_heuristic[i,j] = 2
            filled -= 1
    return sudoku_heuristic

def solve_sudoku_heuristic(sudoku,sudoku_map,sudoku_heuristic = None):
    if sudoku_heuristic is None:
        sudoku_heuristic = np.ones(sudoku.shape,np.int8)
    
    # write zeros where there are numbers already filled in
    solutions = (lambda x: x== 0)(sudoku)
    sudoku_heuristic = np.multiply(solutions,sudoku_heuristic)
    
    start = np.unravel_index(np.argmax(sudoku_heuristic),sudoku_heuristic.shape)
    return solve_sudoku_rek(sudoku,sudoku_map,sudoku_heuristic,start,0)

def solve_sudoku_rek(sudoku,sudoku_map,sudoku_heuristic,curr,num_steps):
    if num_steps < 0:
        print("WARNING: number of steps overflowed, result will not be accurate")
    elif num_steps > 1000000:
        #print (sudoku_heuristic)
        #print()
        #print(sudoku)
        raise AssertionError("number of steps exceeded 1000000")
    
    heuristic = sudoku_heuristic[curr]
    
    for number in range(1,max(sudoku.shape)+1):
        num_steps += 1
        if check_for_availability(sudoku,sudoku_map,number,curr):
            sudoku[curr] = number
            sudoku_heuristic[curr] = 0
            nex = np.unravel_index(np.argmax(sudoku_heuristic),sudoku_heuristic.shape)
            
            if np.amax(sudoku_heuristic) == 0:
                return (True,num_steps,sudoku)
            
            solution = solve_sudoku_rek(sudoku,sudoku_map,sudoku_heuristic,nex,num_steps)
            
            if solution[0]:
                return solution
            else:
                num_steps = solution[1]
            
            sudoku_heuristic[curr] = heuristic
            sudoku[curr] = 0
    return (False,num_steps,sudoku)

def create_sudoku(sudoku_map,filled = 17):
    sudoku = np.zeros(sudoku_map.shape,np.int8)
    sudoku_heuristic = create_heuristic_random(sudoku_map)
    
    solution = solve_sudoku_heuristic(sudoku,sudoku_map,sudoku_heuristic)[2]
    length = max(sudoku_map.shape)
    
    to_leave = np.zeros(sudoku_map.shape,np.int8)
    
    while filled >= 0:
        i = r.randint(0,length - 1)
        j = r.randint(0,length - 1)
        
        if to_leave[i,j] != 1:
            to_leave[i,j] = 1
            filled -= 1
    sudoku = np.multiply(solution,to_leave)
    return (sudoku,solution)
    
    
if __name__ == "__main__":
    sudoku = np.zeros((9,9),np.int8)
    sudoku[0,0] = 5
    sudoku_map = create_normal_sudoku_map()
    