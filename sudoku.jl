# create the colormap for a traditional sudoku, where a 9*9 board is split into 9 3*3 areas of the same colour
function createNormalSudokuMap()
	out = zeros(UInt8,9,9)
	inc = [1 1 1 2 2 2 3 3 3]

	for i in [1,4,7]
		big = [inc;inc;inc]
		inc = inc .+ 3
		out[i:i+2,:] = big
	end

	return out
end

#=
	sudoku -> the sudoku grid, can have some numbers already filled
	sudoku_map -> the colormap for the sudoku, a color cannot have two numbers with the same value
	number -> the number we are trying to insert
	cartesian -> (i,j) touple, where i is the row index and j is the column index
=#
function checkForAvailability(sudoku, sudoku_map, number, cartesian::CartesianIndex{2})
	function checkRowAva(number, row)
		if number in row
			return false
		end
		return true
	end

	row_available = checkRowAva(number,sudoku[cartesian[1],:])
	column_available = checkRowAva(number,sudoku[:,cartesian[2]])

	colour = sudoku_map[cartesian]
	result = map(x -> x == number, sudoku)
	colors = map(x -> x == colour, sudoku_map)

	ultraRes = result .* colors

	if (row_available && column_available && !(true in ultraRes))
		return true
	end
	return false
end

# creates a new sudoku based on the sudoku_map, with "filled" fields filled, (filled is a number, that many fields remain filled)
function createSudoku(sudoku_map,filled = 5)
	sudoku = zeros(Int8,size(sudoku_map))
	# TODO
	return sudoku
end

#=
	sudoku -> the sudoku grid, can have some numbers already filled
	sudoku_map -> the colormap for the sudoku, a color cannot have two numbers with the same value
	sudoku_hevristic -> optional, which fields the sudoku solver prioritizes, if not provided all fields have an equal pripority, the solver will solve up to down, left to right
	returns (solution_found, number of steps, sudoku)
		solution_found -> boolean, weather a solution was found or not
		number of steps -> number of different numbers tried to arrive to the returned sudoku
		sudoku -> the sudoku the program had stored at the end
=#
function solveSudokuHevristic(sudoku,sudoku_map,sudoku_hevristic = nothing)
	function is_zero(x)
		if x == 0
			return 1
		end
		return 0
	end

	if sudoku_hevristic == nothing
		sudoku_hevristic = map(is_zero,sudoku)
	else
		values = map(x -> x == 0,sudoku)
		sudoku_hevristic = sudoku_hevristic .* values
	end

	start = findmax(sudoku_hevristic)[2]
	return solveSudokuRek(sudoku,sudoku_map,sudoku_hevristic,start,Int64(0))
end

#=
	helper function for function solveSudokuHevristic
	curr -> current field being filled, type CartesianIndex(i, j)
=#
function solveSudokuRek(sudoku,sudoku_map,sudoku_hevristic,curr,num_steps)

	if num_steps < 0
		@warn "overflow for number of steps, result will be inaccurate", num_steps
	end

	hevristic = sudoku_hevristic[curr]
	for number in 1:maximum(size(sudoku))
		num_steps += 1
		if checkForAvailability(sudoku,sudoku_map,number,curr)
			sudoku[curr] = number
			sudoku_hevristic[curr] = 0
			next = findmax(sudoku_hevristic)
			
			# solved sudoku
			if next[1] == 0
				return (true,num_steps,sudoku)
			end
			
			solution = solveSudokuRek(sudoku,sudoku_map,sudoku_hevristic,next[2],num_steps)

			# if we found a solution
			if solution[1]
				return solution
			# if we didn't find a solution, change the number of steps to that of the subtree
			else
				num_steps = solution[2]
			end
			# cleanup if a solution was not found
			sudoku_hevristic[curr] = hevristic
			sudoku[curr] = 0
		end
	end
	return (false,num_steps,sudoku)
end

sudoku_map = createNormalSudokuMap()
sudoku = createSudoku(sudoku_map)
println(solveSudokuHevristic(sudoku,sudoku_map))