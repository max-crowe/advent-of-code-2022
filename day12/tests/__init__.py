import unittest
from io import StringIO
from ..src import Map

class MapTest(unittest.TestCase):
	TEST_INPUT = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""
	# Impassable
	TEST_INPUT_2 = """Sabqponm
abcryxxl
accszExk
acatuvwj
abdefghi"""
	# Same as first test case, but with an impassible potential origin
	TEST_INPUT_3 = """aaSabqponm
aaabcryxxl
aaaccszExk
aaacctuvwj
aaabdefghi
aaaaaaaaaa
aaaaaaaaaa
aaaddddaaa
aadbcabaaa
aacbbbbaaa"""
	
	def test_find_best_path_from_fixed_origin(self):
		map_ = Map.read_input(StringIO(self.TEST_INPUT))
		self.assertEqual(
			len(map_.origin.get_shortest_path(map_.destination)),
			31
		)
		map_ = Map.read_input(StringIO(self.TEST_INPUT_2))
		self.assertIsNone(map_.origin.get_shortest_path(map_.destination))
		map_ = Map.read_input(StringIO(self.TEST_INPUT_3))
		self.assertEqual(
			len(map_.origin.get_shortest_path(map_.destination)),
			31
		)
		
	def test_find_best_path_from_any_origin(self):
		map_ = Map.read_input(StringIO(self.TEST_INPUT))
		self.assertEqual(
			len(map_.find_best_path_from_arbitrary_origin(lambda node: node.height == 0)),
			29
		)
		map_ = Map.read_input(StringIO(self.TEST_INPUT_2))
		self.assertIsNone(map_.find_best_path_from_arbitrary_origin(lambda node: node.height == 0))
		map_ = Map.read_input(StringIO(self.TEST_INPUT_3))
		self.assertEqual(
			len(map_.find_best_path_from_arbitrary_origin(lambda node: node.height == 0)),
			29
		)
		