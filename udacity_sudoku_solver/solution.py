from utils import *
import itertools


row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units
#Diagonal units
char = list("ABCDEFGHI")
num1 = list("123456789")
num2 = list("987654321")
diagonal_units= [list(map(lambda a, b: a + b, char, num1))]+ [list(map(lambda a, b: a + b, char, num2))]

# make two diagonal units
# TODO: Update the unit list to add the new diagonal units
unitlist = unitlist + diagonal_units



# Must be called after all units (including diagonals) are added to the unitlist
units = extract_units(unitlist, boxes)
peers = extract_peers(units, boxes)

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    #get position with two values
    pairs = [box for box in values.keys() if len(values[box]) == 2 for unit in unitlist]
    #get all naked twins
    naked_twins = [[box,peer] for box in set(pairs) for peer in peers[box] if values[box] == values[peer]]
    # Eliminate the naked twins as possibilities for their peers
    for box,peer in naked_twins:
        for value in (set(peers[box]) & set(peers[peer])):
            if box != peer:		
                for digit in values[box]:
                    values[value] = values[value].replace(digit,'')          
    return values
    raise NotImplementedError

def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """
    # TODO: Copy your code from the classroom to complete this function
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values
    raise NotImplementedError


def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    """
    # TODO: Copy your code from the classroom to complete this function
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values
    raise NotImplementedError

def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable 
    """
    # TODO: Copy your code from the classroom and modify it to complete this function
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)

        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)
        #
        # Your code here : Use the Naked Twins Strategy 
        values = naked_twins(values) 


        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values
    raise NotImplementedError

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if not values: return False

    # Choose one of the unfilled squares with the fewest possibilities
    unfilled = [(len(v), k) for k, v in values.items() if len(v) > 1]
    if not unfilled:
        return values
    min_box = min(unfilled)[1]

    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    original = values.copy()
    for el in values[min_box]:
        values = original.copy()
        values[min_box] = el
        values = search(values)
        if values:
            return values


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """

    values = grid2values(grid)
    return search(values)


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)

    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')

#References:
#Github Repos
#https://github.com/lfiaschi/udacity-sudoku/blob/master/solution.py
#https://github.com/iacutone/AIND-Sudoku
#https://github.com/davidventuri/udacity-aind/blob/master/sudoku/solution.py
#https://github.com/philferriere/aind-projects/blob/master/sudoku/README.md
#Blogs
#http://norvig.com/sudoku.html
#https://towardsdatascience.com/peter-norvigs-sudoku-solver-25779bb349ce

#        