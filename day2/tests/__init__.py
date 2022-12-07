from unittest import TestCase
from ..src import Play, Outcome

class PlayTestCase(TestCase):
	def test_equality(self):
		self.assertTrue(Play(Play.Choices.ROCK) == Play(Play.Choices.ROCK))
		self.assertTrue(Play(Play.Choices.ROCK) == Play('A'))
		self.assertTrue(Play(Play.Choices.ROCK) == Play('X'))
		self.assertFalse(Play(Play.Choices.PAPER) == Play(Play.Choices.SCISSORS))
		self.assertFalse(Play('B') == Play('Z'))
		
	def test_comparisons(self):
		self.assertTrue(Play(Play.Choices.ROCK) > Play(Play.Choices.SCISSORS))
		self.assertFalse(Play(Play.Choices.SCISSORS) >= Play(Play.Choices.ROCK))
		self.assertTrue(Play(Play.Choices.ROCK) < Play(Play.Choices.PAPER))
		self.assertFalse(Play(Play.Choices.PAPER) > Play(Play.Choices.SCISSORS))
		
	def test_scoring(self):
		self.assertEqual(
			Play.score(Play(Play.Choices.ROCK), Play(Play.Choices.SCISSORS)),
			7
		)
		self.assertEqual(
			Play.score(Play(Play.Choices.PAPER), Play(Play.Choices.PAPER)),
			5
		)
		self.assertEqual(
			Play.score(Play(Play.Choices.SCISSORS), Play(Play.Choices.ROCK)),
			3
		)
		self.assertEqual(
			Play.score(Play(Play.Choices.ROCK), Play(Play.Choices.PAPER)),
			1
		)
		
	def test_choice_for_outcome(self):
		self.assertEqual(
			Play.choose_play_for_outcome(Play(Play.Choices.PAPER), Outcome(Outcome.Choices.DRAW)),
			Play(Play.Choices.PAPER)
		)
		self.assertEqual(
			Play.choose_play_for_outcome(Play(Play.Choices.PAPER), Outcome('Y')),
			Play(Play.Choices.PAPER)
		)
		self.assertEqual(
			Play.choose_play_for_outcome(Play(Play.Choices.ROCK), Outcome(Outcome.Choices.LOSE)),
			Play(Play.Choices.SCISSORS)
		)
		self.assertEqual(
			Play.choose_play_for_outcome(Play(Play.Choices.ROCK), Outcome('X')),
			Play(Play.Choices.SCISSORS)
		)
		self.assertEqual(
			Play.choose_play_for_outcome(Play(Play.Choices.SCISSORS), Outcome(Outcome.Choices.WIN)),
			Play(Play.Choices.ROCK)
		)
		self.assertEqual(
			Play.choose_play_for_outcome(Play(Play.Choices.SCISSORS), Outcome('Z')),
			Play(Play.Choices.ROCK)
		)
		self.assertEqual(
			Play.choose_play_for_outcome(Play(Play.Choices.ROCK), Outcome(Outcome.Choices.WIN)),
			Play(Play.Choices.PAPER)
		)
		self.assertEqual(
			Play.choose_play_for_outcome(Play(Play.Choices.ROCK), Outcome('Z')),
			Play(Play.Choices.PAPER)
		)
		