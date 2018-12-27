from sudoku import check_for_availability,create_sudoku,create_normal_sudoku_map

def presolve(sudoku,sudoku_map,added = 0,num_iter = 0):
    
    solved = True
    
    for i in range(max(sudoku.shape)):
        for j in range(max(sudoku.shape)):
            solutions = set()
            
            for numb in range(1,max(sudoku.shape) + 1):
                num_iter += 1
                if check_for_availability(sudoku, sudoku_map,numb,(i,j)):
                    solutions.add(numb)
            
            if len(solutions) == 1:
                solved = False
                added += 1
                sudoku[i,j] = solutions.pop()
    
    if not solved:
        return presolve(sudoku,sudoku_map,added,num_iter)
    return (sudoku,num_iter,added)
    
    
if __name__ == "__main__":
    sudoku_map = create_normal_sudoku_map()
    sudoku = create_sudoku(sudoku_map,25)[0]
    print(presolve(sudoku,sudoku_map))