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
      if summ < 0:
          raise AssertionError("summ shouldn't be negative")
      #print(summ)
  return summ*1.0 / num_iterations

def plot_time_to_fill_ratio(num_iterations = 10,min_solved = 0, max_solved = 25):
    
    x = [i for i in range(min_solved, max_solved)]
    y = [0 for i in range(min_solved,max_solved)]
    
    for i in range(min_solved,max_solved):
        y[i - min_solved] = average_number_steps_to_solve(num_iterations,i)
        print(i,"th iteration, average:",y[i - min_solved])
    plt.plot(x,y)
    plt.savefig("images/fill_to_num_iter_" + str(num_iterations) + ".svg")
    plt.show()
    
if __name__ == "__main__":
    plot_time_to_fill_ratio(50,0,40)