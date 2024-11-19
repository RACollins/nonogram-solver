# --------------------------------------------------------------------------------------------------
# Nongram solver
# Author: Richard Collins
# --------------------------------------------------------------------------------------------------


###############
### Imports ###
###############

import numpy as np
import argparse
import utils

#################
### Functions ###
#################

###############
### Classes ###
###############


class Board:
    ### Cell states
    UNKNOWN = -1
    FILLED = 0
    BLANK = 1

    ### Initialise empty board
    def __init__(self, n_rows: int, n_cols: int):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.grid = np.zeros((n_rows, n_cols), dtype=int)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Nonogram Solver")
    parser.add_argument("puzzle_file", type=str, help="Path to the puzzle text file")
    args = parser.parse_args()

    ### Generate config from the input file
    config = utils.generate_config(args.puzzle_file)

    ### Create board with the parsed size
    board = Board(config["n_rows"], config["n_cols"])

    print(board.grid)
