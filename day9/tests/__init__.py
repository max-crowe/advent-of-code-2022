from io import StringIO
from unittest import TestCase
from ..src import Rope

class RopeTestCase(TestCase):
	TEST_STREAM = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""
	
	def test_simple_tail_position_count(self):
		rope = Rope(2)
		rope.read_moves_from_stream(StringIO(self.TEST_STREAM))
		self.assertEqual(rope.tail.positions_visited, 13)
		
	def test_complex_tail_position_count(self):
		rope = Rope(10)
		rope.read_moves_from_stream(StringIO(self.TEST_STREAM))
		self.assertEqual(rope.tail.positions_visited, 1)
		moves = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""
		rope = Rope(10)
		rope.read_moves_from_stream(StringIO(moves))
		self.assertEqual(rope.tail.positions_visited, 36)
		