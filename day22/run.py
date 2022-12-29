#!/usr/bin/env python
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.resolve()))
from day22.src import Map, Trail

if __name__ == "__main__":
	with open(sys.argv[1]) as input_data:
		map_ = Map.from_input(input_data)
		trail = Trail.from_input(input_data.readline())
	print(map_.follow_trail(trail))