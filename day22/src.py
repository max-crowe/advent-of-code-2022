from enum import IntEnum
from common import BaseMap, Point

WALL = object()

class Directions(IntEnum):
	RIGHT = 0
	DOWN = 1
	LEFT = 2
	UP = 3
	
	@classmethod
	def as_arrow(cls, value):
		if value is cls.UP:
			return '^'
		if value is cls.RIGHT:
			return '>'
		if value is cls.DOWN:
			return 'v'
		return '<'
	
class Row:
	def __init__(self, offset, data):
		self.offset = offset
		self.data = [WALL if char == '#' else None for char in data]
		
	def _get_true_index(self, idx):
		idx -= self.offset
		if idx < 0 or idx >= len(self.data):
			raise IndexError(idx + self.offset)
		return idx
		
	def __len__(self):
		return self.offset + len(self.data)
		
	def __getitem__(self, idx):
		return self.data[self._get_true_index(idx)]
		
	def __setitem__(self, idx, value):
		self.data[self._get_true_index(idx)] = value
		
	@classmethod
	def from_input(cls, line):
		try:
			space_offset = line.index('.')
		except ValueError:
			raise ValueError('No space found in line')
		try:
			wall_offset = line.index('#')
		except ValueError:
			offset = space_offset
		else:
			offset = min(space_offset, wall_offset)
		return cls(offset, line[offset:])
	
class Map(BaseMap):
	def __init__(self):
		super().__init__()
		self.column_data = []
		self.boundary_points = None
		self.position = None
		self.direction = Directions.RIGHT
		self.steps_followed = {}
		
	def __str__(self):
		str_rows = []
		for y_index, row in enumerate(self.rows):
			str_row = ' ' * row.offset
			for x_index, point in enumerate(row.data, row.offset):
				current_point = Point(x_index, y_index)
				if self.position == current_point:
					str_row += Directions.as_arrow(self.direction)
				elif current_point in self.steps_followed:
					str_row += Directions.as_arrow(self.steps_followed[current_point])
				elif point is WALL:
					str_row += '#'
				else:
					str_row += '.'
			str_rows.append(str_row)
		return '\n'.join(str_rows)
		
	@classmethod
	def from_input(cls, input_stream, as_cube=False):
		map_ = cls()
		max_length = 0
		for y_index, line in enumerate(input_stream):
			line = line.rstrip()
			if not len(line):
				break
			row = Row.from_input(line)
			if map_.position is None:
				map_.position = Point(line.index('.'), y_index)
			map_.rows.append(row)
			row_length = len(row)
			if row_length > max_length:
				max_length = row_length
		max_height = 0
		for x in range(max_length):
			length = 0
			offset = 0
			for y in range(len(map_.rows)):
				try:
					map_[Point(x, y)]
				except IndexError:
					if length:
						break
					offset += 1
				else:
					if not length:
						length = offset
					length += 1
			map_.column_data.append((offset, length))
			if length > max_height:
				max_height = length
		if as_cube:
			cube_face_length = int(max(max_length, max_height) / 4)
			map_.boundary_points = {}
			for x in range(0, max_length, cube_face_length):
				for y in (map_.column_data[x][0], map_.column_data[x][1] - 1):
					for x_offset in range(cube_face_length):
						boundary_point = Point(x + x_offset, y)
						direction = Directions.UP if y == map_.column_data[x][0] else Directions.DOWN
						if y == 0:
							if x - cube_face_length <= 0:
								adjoining_point = Point(
									0, cube_face_length * 3 + x_offset - 1
								)
								adjoining_direction = Directions.RIGHT
							elif x >= cube_face_length * 2:
								adjoining_point = Point(
									x_offset,
									max_height - 1
								)
								adjoining_direction = Directions.UP
							else:
								adjoining_point = Point(
									x - cube_face_length - x_offset - 1,
									cube_face_length
								)
								adjoining_direction = Directions.DOWN
						else:
							if x + cube_face_length * 3 < max_length:
								if y == map_.column_data[x][0]:
									adjoining_direction = Directions.DOWN
									adjoining_point = Point(
										cube_face_length * 3 - x_offset - 1,
										0
									)
								else:
									adjoining_direction = Directions.LEFT
									adjoining_point = Point(
										max_length - 1, x_offset
									)
							elif x + cube_face_length * 2 < max_length:
								if y == max_height - 1:
									adjoining_direction = Directions.LEFT
									adjoining_point = Point(
										max_length, x_offset
									)
								else:
									adjoining_direction = Directions.RIGHT
									if y == map_.column_data[x][0]:
										adjoining_y = y - (cube_face_length - x_offset)
									else:
										adjoining_y = y + (cube_face_length - x_offset)
								adjoining_point = Point(
									x + cube_face_length,
									adjoining_y
								)
							elif y == map_.column_data[x][0]:
								adjoining_point = Point(
									x - 1,
									y - x_offset - 1
								)
								adjoining_direction = Directions.LEFT
							elif y == max_height - 1:
								if x + cube_face_length < max_length:
									adjoining_direction = Directions.UP
									adjoining_point = Point(
										x - cube_face_length - x_offset - 1,
										y - cube_face_length
									)
								else:
									adjoining_direction = Directions.RIGHT
									adjoining_point = Point(
										0,
										y - cube_face_length * 2 + (cube_face_length - x_offset)
									)
							else:
								adjoining_direction = Directions.LEFT
								adjoining_point = Point(
									x - 1,
									y + x_offset + 1
								)	
						map_.add_boundary_point(
							boundary_point,
							direction,
							adjoining_point,
							adjoining_direction
						)
			for y in range(0, max_height, cube_face_length):
				for x in (map_.rows[y].offset, len(map_.rows[y]) - 1):
					for y_offset in range(cube_face_length):
						boundary_point = Point(x, y + y_offset)
						direction = Directions.LEFT if x == map_.rows[y].offset else Directions.RIGHT
						if direction in map_.boundary_points.get(boundary_point, {}):
							continue
						adjoining_point = None
						adjoining_direction = None
						if x == 0:
							if y + cube_face_length == max_height:
								adjoining_point = Point(
									cube_face_length + y_offset + 1,
									0
								)
								adjoining_direction = Directions.DOWN
							else:
								adjoining_point = Point(
									cube_face_length,
									cube_face_length - 1 - y_offset
								)
								adjoining_direction = Directions.RIGHT
						elif y >= cube_face_length * 2:
							adjoining_point = Point(
								max_length - 1,
								cube_face_length - 1 - y_offset
							)
							adjoining_direction = Directions.LEFT
						if adjoining_point:
							map_.add_boundary_point(
								boundary_point,
								direction,
								adjoining_point,
								adjoining_direction
							)
		return map_
		
	def add_boundary_point(self, point, direction, adjoining_point, adjoining_direction):
		try:
			point_index = self.boundary_points[point]
		except KeyError:
			point_index = self.boundary_points[point] = {}
		if direction not in point_index:
			point_index[direction] = (adjoining_point, adjoining_direction)
			opposite_direction = direction + 2
			if opposite_direction > 3:
				opposite_direction -= 4
			opposite_adjoining_direction = adjoining_direction + 2
			if opposite_adjoining_direction > 3:
				opposite_adjoining_direction -= 4
			self.add_boundary_point(
				adjoining_point,
				Directions(opposite_adjoining_direction),
				point,
				Directions(opposite_direction)
			)
			
	def get_next_position(self):
		next_position = None
		next_direction = None
		if self.boundary_points:
			try:
				next_position, next_direction = self.boundary_points[self.position][self.direction]
			except KeyError:
				pass
		if next_position is None:
			is_horizontal = self.direction is Directions.RIGHT or self.direction is Directions.LEFT
			if self.direction is Directions.RIGHT or self.direction is Directions.DOWN:
				position_diff = 1
			else:
				position_diff = -1
			if is_horizontal:
				next_position = Point(
					self.position.x + position_diff,
					self.position.y
				)
			else:
				next_position = Point(
					self.position.x,
					self.position.y + position_diff
				)
				if next_position.y < 0:
					next_position.y = self.column_data[next_position.x][1] - 1
		try:
			obj_at_position = self[next_position]
		except IndexError:
			if self.boundary_points:
				raise
			if self.direction is Directions.RIGHT:
				next_position.x = self.rows[next_position.y].offset
			elif self.direction is Directions.LEFT:
				next_position.x = len(self.rows[next_position.y]) - 1
			elif self.direction is Directions.DOWN:
				next_position.y = self.column_data[next_position.x][0]
			else:
				next_position.y = self.column_data[next_position.x][1] - 1
			obj_at_position = self[next_position]
		if obj_at_position is not WALL:
			if next_direction is not None:
				self.direction = next_direction
			return next_position
			
	def get_next_direction(self, direction):
		assert direction is Directions.RIGHT or direction is Directions.LEFT, \
			"Can only rotate clockwise or counterclockwise"
		if direction is Directions.RIGHT:
			new_direction = int(self.direction) + 1
			return Directions(new_direction) if new_direction < 4 else Directions.RIGHT
		new_direction = int(self.direction) - 1
		return Directions(new_direction) if new_direction >= 0 else Directions.UP
		
	def follow_trail(self, trail):
		self.set_trail(trail)
		self.step_through_trail()
		return (1000 * (self.position.y + 1)) + (4 * (self.position.x + 1)) + int(self.direction)
		
	def set_trail(self, trail):
		self.trail_iterator = iter(trail)
	
	def step_through_trail(self, steps=None, verbose=False):
		steps_consumed = 0
		while True:
			try:
				instruction = next(self.trail_iterator)
			except StopIteration:
				break
			if verbose:
				print(instruction)
			if isinstance(instruction, Directions):
				self.direction = self.get_next_direction(instruction)
			else:
				for i in range(instruction):
					if next_position := self.get_next_position():
						self.position = next_position
						self.steps_followed[self.position] = self.direction
					else:
						break
			steps_consumed += 1
			if steps is not None and steps_consumed == steps:
				break
			
class Trail:
	def __init__(self):
		self.data = []
		
	def __iter__(self):
		yield from self.data
		
	@classmethod
	def from_input(cls, line):
		pos = 0
		trail = cls()
		while True:
			try:
				next_right = line.index('R', pos)
			except ValueError:
				next_right = None
			try:
				next_left = line.index('L', pos)
			except ValueError:
				next_left = None
			if next_right and next_left:
				next_direction = min(next_right, next_left)
			elif next_right:
				next_direction = next_right
			elif next_left:
				next_direction = next_left
			else:
				next_direction = None
			if next_direction:
				steps = int(line[pos:next_direction])
			else:
				steps = int(line[pos:])
			trail.data.append(steps)
			if next_direction:
				trail.data.append(Directions.RIGHT if line[next_direction] == 'R' else Directions.LEFT)
				pos = next_direction + 1
			else:
				break
		return trail
	