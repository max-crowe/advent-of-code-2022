#!/usr/bin/env python
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.resolve()))
from day9.src import Rope

if __name__ == "__main__":
	rope = Rope(int(sys.argv[1]))
	with open(sys.argv[2]) as reader:
		rope.read_moves_from_stream(reader)
	print("Tail positions visited: {}".format(rope.tail.positions_visited))