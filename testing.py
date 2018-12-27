from sudoku import solve_sudoku_heuristic, create_sudoku, create_normal_sudoku_map,create_different_color_map
import matplotlib.pyplot as plt
from better_solve import presolve


def average_number_steps_to_solve(sudoku_map = None,num_iterations = 10,filled = 25,presol = False):
  """
  Calculates the average amount of steps needed to solve a sudoku with "filled"
  spaces filled
  """
  summ = 0
  presolve_iter = 0
  i = 1
  while i <= num_iterations:
      how_many = 0
      if sudoku_map is None:
          sudoku_map = create_normal_sudoku_map()
      
      try:
          sudoku = create_sudoku(sudoku_map,filled)[0]
          if presol:
              sudoku,presolve_iter,how = presolve(sudoku,sudoku_map)
              how_many += how
          solution = solve_sudoku_heuristic(sudoku,sudoku_map)
      except AssertionError:
          continue
      print("iter",i,"/",num_iterations, "how many:",how_many)
      i += 1
      summ += solution[1]
      summ += presolve_iter
      if summ < 0:
          raise AssertionError("summ shouldn't be negative")
      #print(summ)
  return summ*1.0 / num_iterations

def plot_time_to_fill_ratio(sudoku_map = None, num_iterations = 70,min_solved = 0, max_solved = 40,presolve = False):
    if sudoku_map is None:
        sudoku_map = create_normal_sudoku_map()
    
    x = [i for i in range(min_solved, max_solved)]
    y = [0 for i in range(min_solved,max_solved)]
    
    for i in range(min_solved,max_solved):
        y[i - min_solved] = average_number_steps_to_solve(sudoku_map,num_iterations,i,presolve)
        print(i,"th iteration, average:",y[i - min_solved])
    plt.plot(x,y)
    plt.savefig("images/fill_to_num_iter_" + str(num_iterations) + ".svg")
    plt.show()

def plot_time_to_size_ratio(num_iterations = 70, min_solved = 3, max_solved = 15,fill_per = 0.25):
    
    x = [i for i in range(min_solved, max_solved)]
    y = [0 for i in range(min_solved,max_solved)]
    
    for i in range(min_solved,max_solved):
        sudoku_map = create_different_color_map(i)
        to_fill = int(i*i * fill_per) + 1
        y[i - min_solved] = average_number_steps_to_solve(sudoku_map,num_iterations,to_fill)
        print(i,"th iteration, average:",y[i - min_solved])
    plt.plot(x,y)
    plt.savefig("images/size_to_num_iter_" + str(num_iterations)+ "_filled_" + str(fill_per) + ".svg")
    plt.show()

if __name__ == "__main__":
    plot_time_to_fill_ratio(presolve=False)
