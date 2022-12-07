#!/usr/bin/env python
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.resolve()))
from day2.src import Play

if __name__ == '__main__':
	cumulative_score = 0
	with open(sys.argv[1]) as input_file:
		for line in input_file:
			opponent_choice, _, my_choice = line.strip().partition(' ')
			cumulative_score += Play.score(
				Play(my_choice), Play(opponent_choice)
			)
	print(cumulative_score)