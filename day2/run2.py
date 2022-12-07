#!/usr/bin/env python
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.resolve()))
from day2.src import Play, Outcome

if __name__ == '__main__':
	cumulative_score = 0
	with open(sys.argv[1]) as input_file:
		for line in input_file:
			opponent_choice, _, outcome_option = line.strip().partition(' ')
			opponent_play = Play(opponent_choice)
			cumulative_score += Play.score(
				Play.choose_play_for_outcome(opponent_play, Outcome(outcome_option)), opponent_play
			)
	print(cumulative_score)