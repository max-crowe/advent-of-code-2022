#!/usr/bin/env python
import sys
from argparse import ArgumentParser
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.resolve()))
from day23.src import Map

if __name__ == "__main__":
	parser = ArgumentParser()
	parser.add_argument('input', type=open)
	parser.add_argument('rounds', type=int, nargs='?')
	args = parser.parse_args()
	if args.rounds:
		map_ = Map.from_input(args.input, args.rounds)
		for i in range(args.rounds):
			map_.do_round()
		print(map_.empty_spaces_within_min_bounding_rectangle)
	else:
		map_ = Map.from_input(args.input, 50)
		rounds = 1
		while moves := map_.do_round():
			rounds += 1
			if rounds % 100 == 0:
				print(f"After {rounds} rounds:\n{map_}\n")
		print(rounds)