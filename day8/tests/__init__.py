from io import StringIO
from unittest import TestCase
from ..src import Grid

class GridTestCase(TestCase):
	TEST_STREAM = """
30373
25512
65332
33549
35390
"""
	
	def test_visibility_count(self):
		grid = Grid(StringIO(self.TEST_STREAM))
		self.assertEqual(grid.count_visible_trees(), 21)
		
	def test_scenic_score(self):
		grid = Grid(StringIO(self.TEST_STREAM))
		grid.compute_scenic_scores()
		self.assertEqual(grid.grid[1][2].score, 4)
		self.assertEqual(grid.grid[3][2].score, 8)