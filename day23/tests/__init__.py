import unittest
from io import StringIO
from ..src import Directions, Map, Point

class MapTestCase(unittest.TestCase):
	TEST_INPUT_1 = """##
#.
..
##"""

	TEST_INPUT_2 = """....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#.."""

	def test_simple(self):
		map_ = Map.from_input(StringIO(self.TEST_INPUT_1), 3)
		self.assertEqual(
			map_.min_bounding_point, Point(3, 3)
		)
		self.assertEqual(
			map_.max_bounding_point, Point(4, 6)
		)
		self.assertEqual(
			map_.empty_spaces_within_min_bounding_rectangle, 3
		)
		self.assertTrue(
			map_.is_occupied(Point(3, 3))
		)
		self.assertTrue(
			map_.is_occupied(Point(4, 3))
		)
		self.assertTrue(
			map_.is_occupied(Point(3, 4))
		)
		self.assertFalse(
			map_.is_occupied(Point(4, 4))
		)
		self.assertFalse(
			map_.is_occupied(Point(3, 5))
		)
		self.assertFalse(
			map_.is_occupied(Point(4, 5))
		)
		self.assertTrue(
			map_.is_occupied(Point(3, 6))
		)
		self.assertTrue(
			map_.is_occupied(Point(4, 6))
		)
		map_.do_round()
		self.assertIs(map_.current_start_direction, Directions.N)
		self.assertEqual(
			map_.min_bounding_point, Point(3, 2)
		)
		self.assertEqual(
			map_.max_bounding_point, Point(4, 6)
		)
		self.assertEqual(
			map_.empty_spaces_within_min_bounding_rectangle, 5
		)
		self.assertTrue(
			map_.is_occupied(Point(3, 2))
		)
		self.assertTrue(
			map_.is_occupied(Point(4, 2))
		)
		self.assertFalse(
			map_.is_occupied(Point(3, 3))
		)
		self.assertFalse(
			map_.is_occupied(Point(4, 3))
		)
		self.assertTrue(
			map_.is_occupied(Point(3, 4))
		)
		self.assertFalse(
			map_.is_occupied(Point(4, 4))
		)
		self.assertFalse(
			map_.is_occupied(Point(3, 5))
		)
		self.assertTrue(
			map_.is_occupied(Point(4, 5))
		)
		map_.do_round()
		self.assertIs(map_.current_start_direction, Directions.S)
		self.assertEqual(
			map_.min_bounding_point, Point(2, 3)
		)
		self.assertEqual(
			map_.max_bounding_point, Point(5, 7)
		)
		self.assertEqual(
			map_.empty_spaces_within_min_bounding_rectangle, 15
		)
		map_.do_round()
		self.assertIs(map_.current_start_direction, Directions.W)
		self.assertEqual(
			map_.min_bounding_point, Point(1, 2)
		)
		self.assertEqual(
			map_.max_bounding_point, Point(5, 7)
		)
		self.assertEqual(
			map_.empty_spaces_within_min_bounding_rectangle, 25
		)
		
	def test_medium(self):
		map_ = Map.from_input(StringIO(self.TEST_INPUT_2), 10)
		for i in range(10):
			map_.do_round()
		self.assertEqual(map_.empty_spaces_within_min_bounding_rectangle, 110)