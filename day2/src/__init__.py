from enum import IntEnum

class Outcome:
	class Choices(IntEnum):
		LOSE = 0
		DRAW = 3
		WIN = 6
		
	CHOICE_MAP = {
		'X': Choices.LOSE,
		'Y': Choices.DRAW,
		'Z': Choices.WIN
	}
		
	def __init__(self, choice_or_code):
		if not isinstance(choice_or_code, self.Choices):
			choice_or_code = self.CHOICE_MAP[choice_or_code]
		self.choice = choice_or_code

class Play:
	class Choices(IntEnum):
		ROCK = 1
		PAPER = 2
		SCISSORS = 3
	
	CHOICE_MAP = {
		'A': Choices.ROCK,
		'B': Choices.PAPER,
		'C': Choices.SCISSORS,
		'X': Choices.ROCK,
		'Y': Choices.PAPER,
		'Z': Choices.SCISSORS
	}
	
	def __init__(self, choice_or_code):
		if not isinstance(choice_or_code, self.Choices):
			choice_or_code = self.CHOICE_MAP[choice_or_code]
		self.choice = choice_or_code
		
	def __gt__(self, other):
		if self.choice is self.Choices.ROCK and other.choice is self.Choices.SCISSORS:
			return True
		if self.choice is self.Choices.SCISSORS and other.choice is self.Choices.ROCK:
			return False
		return self.choice.value > other.choice.value
		
	def __ge__(self, other):
		return self == other or self > other
		
	def __eq__(self, other):
		return self.choice is other.choice
		
	def __lt__(self, other):
		return other > self
		
	def __le__(self, other):
		return self == other or other > self

	@classmethod
	def score(cls, my_play, opponent_play):
		if my_play > opponent_play:
			base_score = int(Outcome.Choices.WIN)
		elif my_play == opponent_play:
			base_score = int(Outcome.Choices.DRAW)
		else:
			base_score = int(Outcome.Choices.LOSE)
		return base_score + my_play.choice.value
		
	@classmethod
	def choose_play_for_outcome(cls, opponent_play, outcome):
		assert isinstance(opponent_play, cls) and isinstance(outcome, Outcome)
		sorted_choices = sorted(cls.Choices)
		opponent_play_index = sorted_choices.index(opponent_play.choice)
		if outcome.choice is Outcome.Choices.WIN:
			choice = sorted_choices[0] if opponent_play_index + 1 == len(sorted_choices) else sorted_choices[opponent_play_index + 1]
		elif outcome.choice is Outcome.Choices.DRAW:
			choice = opponent_play.choice
		else:
			choice = sorted_choices[opponent_play_index - 1]
		return cls(choice)
			
		
