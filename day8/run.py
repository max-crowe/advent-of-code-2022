#!/usr/bin/env python
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.resolve()))
from day8.src import Grid

if __name__ == "__main__":
	with open(sys.argv[1]) as reader:
		grid = Grid(reader)
	print("Visible trees: {}".format(grid.count_visible_trees()))
	print("Best scenic score: {}".format(grid.get_best_scenic_score()))