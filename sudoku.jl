function checkRowAva(number, row)
	if number in row
		return false
	end
	return true
end

function createNormalSudokuMap()
	out = zeros(9,9)
	inc = [1 1 1 2 2 2 3 3 3]

	for i in [1,4,7]
		big = [inc;inc;inc]
		inc = inc .+ 3
		out[i:i+2,:] = big
	end

	return out
end

function checkForAvailability(number, row, column, sudoku_map, sudoku)
	row_available = checkRowAva(number,sudoku[row,:])
	column_available = checkRowAva(number,sudoku[:,row])

	colour = sudoku_map[row,column]
	result = map(x -> x == number, sudoku)
	colors = map(x -> x == colour, sudoku_map)

	ultraRes = result .* colors

	if true in ultraRes
		return false
	end
	return true
end

length = 9
sudoku = zeros(length,length)
sudoku[1,4] = 1
sudoku_map = createNormalSudokuMap()