from sudoku import solve_sudoku_heuristic, create_sudoku, create_normal_sudoku_map
import matplotlib.pyplot as plt


def average_number_steps_to_solve(num_iterations = 10,filled = 17):
  """
  Calculates the average amount of steps needed to solve a sudoku with "filled"
  spaces filled
  """
  summ = 0
  i = num_iterations
  while i >= 0:
      sudoku_map = create_normal_sudoku_map()
      i -= 1
      
      try:
          sudoku = create_sudoku(sudoku_map,filled)[0]
          
          solution = solve_sudoku_heuristic(sudoku,sudoku_map)
      except AssertionError:
          i += 1
          continue
      summ += solution[1]
      #print(summ)
  return summ*1.0 / num_iterations

def plot_time_to_fill_ratio(num_iterations = 10):
    
    x = [i for i in range(25)]
    y = [0 for i in range(25)]
    
    for i in range(25):
        y[i] = average_number_steps_to_solve(num_iterations,i)
        print(i,"th iteration, average:",y[i])
    plt.plot(x,y)
    
if __name__ == "__main__":
    plot_time_to_fill_ratio(50)