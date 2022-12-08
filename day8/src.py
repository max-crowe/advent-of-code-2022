class Cell:
	def __init__(self, height):
		self.height = int(height)
		self.visible_from_outside = False
		self.score = None
		
	def __str__(self):
		if self.visible_from_outside:
			return '[{}]'.format(self.height)
		return '({})'.format(self.height)
		
	def __int__(self):
		return self.height

class Grid:
	def __init__(self, reader):
		self.grid = []
		self.x_size = None
		self.y_size = 0
		for line in reader:
			row = [Cell(c) for c in line.strip()]
			if not row:
				continue
			self.grid.append(row)
			self.y_size += 1
			if self.x_size is None:
				self.x_size = len(row)
			else:
				assert len(row) == self.x_size, \
					"Mismatched length at line {}".format(self.y_size)
					
	def __str__(self):
		return "\n".join(
			', '.join(str(cell) for cell in row) for row in self.grid
		)
					
	def scan_range_from_outside(self, fixed_idx, is_ascending, is_horizontal):
		threshold = -1
		if is_horizontal:
			if is_ascending:
				range_ = range(self.x_size)
			else:
				range_ = range(self.x_size - 1, -1, -1)
		else:
			if is_ascending:
				range_ = range(self.y_size)
			else:
				range_ = range(self.y_size - 1, -1, -1)
		for variable_idx in range_:
			if is_horizontal:
				x, y = variable_idx, fixed_idx
			else:
				x, y = fixed_idx, variable_idx
			height = int(self.grid[y][x])
			if height > threshold:
				self.grid[y][x].visible_from_outside = True
				threshold = height
				
	def get_viewing_distance(self, ref_x, ref_y, is_ascending, is_horizontal):
		viewing_distance = 0
		ref_height = int(self.grid[ref_y][ref_x])
		if is_ascending:
			if is_horizontal:
				range_ = range(ref_x + 1, self.x_size)
			else:
				range_ = range(ref_y + 1, self.y_size)
		else:
			if is_horizontal:
				range_ = range(ref_x - 1, -1, -1)
			else:
				range_ = range(ref_y - 1, -1, -1)
		for variable_idx in range_:
			if is_horizontal:
				x, y = variable_idx, ref_y
			else:
				x, y = ref_x, variable_idx
			viewing_distance += 1
			if int(self.grid[y][x]) >= ref_height:
				break
		return viewing_distance
					
	def count_visible_trees(self):
		for x in range(self.x_size):
			self.scan_range_from_outside(x, True, False)
			self.scan_range_from_outside(x, False, False)
		for y in range(self.y_size):
			self.scan_range_from_outside(y, False, True)
			self.scan_range_from_outside(y, True, True)
		return sum(
			len(list(filter(lambda c: c.visible_from_outside, self.grid[y]))) for y in range(self.y_size)
		)
		
	def compute_scenic_scores(self):
		for col_idx in range(self.x_size):
			for row_idx in range(self.y_size):
				if self.grid[row_idx][col_idx].score is None:
					up_score = self.get_viewing_distance(col_idx, row_idx, False, False)
					down_score = self.get_viewing_distance(col_idx, row_idx, True, False)
					left_score = self.get_viewing_distance(col_idx, row_idx, False, True)
					right_score = self.get_viewing_distance(col_idx, row_idx, True, True)
					self.grid[row_idx][col_idx].score = up_score * down_score * left_score * right_score
					
	def get_best_scenic_score(self):
		self.compute_scenic_scores()
		candidates = []
		for x in range(self.x_size):
			for y in range(self.y_size):
				candidates.append(self.grid[y][x])
		candidates.sort(key=lambda cell: cell.score, reverse=True)
		return candidates[0].score
		