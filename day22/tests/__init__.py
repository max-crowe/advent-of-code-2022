import unittest
from io import StringIO
from ..src import Directions, Map, Point, Trail, WALL

class MapTestCase(unittest.TestCase):
	TEST_INPUT = """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.
        
10R5L5R10L4R5L5"""
	
	def test_input_parsing(self):
		test_input = StringIO(self.TEST_INPUT)
		map_ = Map.from_input(test_input)
		for i in range(0, 4):
			self.assertEqual(
				len(map_.rows[i]),
				12,
				msg=f'Unexpected row length at index {i}'
			)
			self.assertEqual(
				map_.rows[i].offset,
				8,
				msg=f'Unexpected row offset at index {i}'
			)
		for i in range(4, 8):
			self.assertEqual(
				len(map_.rows[i]),
				12,
				msg=f'Unexpected row length at index {i}'
			)
			self.assertEqual(
				map_.rows[i].offset,
				0,
				msg=f'Unexpected row offset at index {i}'
			)
		for i in range(8, 12):
			self.assertEqual(
				len(map_.rows[i]),
				16,
				msg=f'Unexpected row length at index {i}'
			)
			self.assertEqual(
				map_.rows[i].offset,
				8,
				msg=f'Unexpected row offset at index {i}'
			)
		for i in range(0, 8):
			self.assertEqual(
				map_.column_data[i],
				(4, 8),
				msg=f'Unexpected column length and/or offset at index {i}'
			)
		for i in range(8, 12):
			self.assertEqual(
				map_.column_data[i],
				(0, 12),
				msg=f'Unexpected column length and/or offset at index {i}'
			)
		for i in range(12, 16):
			self.assertEqual(
				map_.column_data[i],
				(8, 12),
				msg=f'Unexpected column length and/or offset at index {i}'
			)
		with self.assertRaises(IndexError):
			map_[Point(0, 0)]
		with self.assertRaises(IndexError):
			map_[Point(7, 3)]
		self.assertIs(map_[Point(11, 0)], WALL)
		self.assertIsNone(map_[Point(8, 0)])
		self.assertIsNone(map_[Point(1, 4)])
		self.assertIs(map_[Point(3, 4)], WALL)
		with self.assertRaises(IndexError):
			map_[Point(7, 8)]
		self.assertIs(map_[Point(14, 11)], WALL)
		self.assertIsNone(map_[Point(15, 11)])
		with self.assertRaises(IndexError):
			map_[Point(16, 12)]
		self.assertEqual(map_.position, Point(8, 0))
		self.assertEqual(map_.direction, Directions.RIGHT)
		trail = Trail.from_input(test_input.readline())
		self.assertEqual(list(trail), [
			10,
			Directions.RIGHT,
			5,
			Directions.LEFT,
			5,
			Directions.RIGHT,
			10,
			Directions.LEFT,
			4,
			Directions.RIGHT,
			5,
			Directions.LEFT,
			5
		])
		
	def test_position_calculation(self):
		map_ = Map.from_input(StringIO(self.TEST_INPUT))
		self.assertEqual(map_.get_next_position(), Point(9, 0))
		map_.direction = Directions.DOWN
		self.assertEqual(map_.get_next_position(), Point(8, 1))
		map_.direction = Directions.LEFT
		self.assertIsNone(map_.get_next_position())
		map_.direction = Directions.UP
		self.assertEqual(map_.get_next_position(), Point(8, 11))
		map_.position = Point(2, 4)
		map_.direction = Directions.RIGHT
		self.assertIsNone(map_.get_next_position())
		map_.direction = Directions.UP
		self.assertEqual(map_.get_next_position(), Point(2, 7))
		
	def test_follow_trail(self):
		test_input = StringIO(self.TEST_INPUT)
		map_ = Map.from_input(test_input)
		password = map_.follow_trail(Trail.from_input(test_input.readline()))
		self.assertEqual(password, 6032)
		self.assertEqual(map_.position, Point(7, 5))
		self.assertIs(map_.direction, Directions.RIGHT)
		
	def test_follow_trail_as_cube(self):
		test_input = StringIO(self.TEST_INPUT)
		map_ = Map.from_input(test_input, as_cube=True)
		password = map_.follow_trail(Trail.from_input(test_input.readline()))
		self.assertEqual(password, 5031)
		self.assertEqual(map_.position, Point(6, 4))
		self.assertIs(map_.direction, Directions.UP)
		
	