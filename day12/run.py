#!/usr/bin/env python
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.resolve()))
from day12.src import Map

if __name__ == "__main__":
	with open(sys.argv[1]) as input_file:
		map_ = Map.read_input(input_file)
	print('Best path from given origin has {} steps'.format(
		len(map_.origin.get_shortest_path(map_.destination))
	))
	print('Best path from any origin with lowest height has {} steps'.format(
		len(map_.find_best_path_from_arbitrary_origin(lambda node: node.height == 0))
	))
	