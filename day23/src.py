from copy import deepcopy
from enum import IntFlag
from itertools import cycle

class Directions(IntFlag):
	N = 2
	E = 4
	S = 8
	W = 16

class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		
	def __str__(self):
		return str((self.x, self.y))
		
	def __repr__(self):
		return str(self)
		
	def __hash__(self):
		return hash((self.x, self.y))
		
	def __eq__(self, other):
		return (self.x, self.y) == (other.x, other.y)
	
class Occupant:
	def __init__(self, map_, initial_coords):
		self.map = map_
		self.coords = initial_coords
		
	def has_adjacent_occupant(self):
		for ns_direction in (Directions.N, Directions.S):
			if self.map.is_occupied(self.map.get_destination_coordinates(
				self.coords, ns_direction
			)):
				return True
			for ew_direction in (Directions.E, Directions.W):
				if self.map.is_occupied(self.map.get_destination_coordinates(
					self.coords, ns_direction | ew_direction
				)):
					return True
		for ew_direction in (Directions.E, Directions.W):
			if self.map.is_occupied(self.map.get_destination_coordinates(
				self.coords, ew_direction
			)):
				return True
		return False
		
	def propose_move(self):
		if self.has_adjacent_occupant():
			for direction in self.map.current_directions_order:
				proposal_coords = self.map.get_destination_coordinates(self.coords, direction)
				if not self.map.is_occupied(proposal_coords, direction):
					return proposal_coords

class Map:
	def __init__(self):
		self.rows = []
		self.occupants = []
		self.min_bounding_point = None
		self.max_bounding_point = None
		self.directions_order = (Directions.N, Directions.S, Directions.W, Directions.E)
		self.direction_cycle = iter(cycle(self.directions_order))
		self.current_start_direction = None
		
	def __str__(self):
		return '\n'.join(''.join('.' if cell is None else '#' for cell in row) for row in self.rows)
		
	def __getitem__(self, coords):
		return self.rows[coords.y][coords.x]
		
	def __setitem__(self, coords, occupant):
		self.rows[coords.y][coords.x] = occupant
		
	@classmethod
	def from_input(cls, input_data, padding):
		map_ = cls()
		padding_rows = []
		for i in range(padding):
			padding_rows.append([])
		map_.rows.extend(padding_rows)
		min_x, min_y, max_x, max_y = None, None, None, None
		for y_idx, line in enumerate(input_data, padding):
			row = []
			map_.rows.append(row)
			row.extend([None] * padding)
			for x_idx, char in enumerate(line.strip(), padding):
				if char == '.':
					row.append(None)
				elif char == '#':
					occupant = Occupant(map_, Point(x_idx, y_idx))
					map_.occupants.append(occupant)
					row.append(occupant)
					if min_x is None or x_idx < min_x:
						min_x = x_idx
					if max_x is None or x_idx > max_x:
						max_x = x_idx
					if min_y is None:
						min_y = y_idx
					max_y = y_idx
				else:
					raise ValueError(f'Unexpected character {char} in input data')
			row.extend([None] * padding)
		for row in padding_rows:
			row.extend([None] * len(map_.rows[-1]))
		map_.rows.extend(deepcopy(padding_rows))
		assert all((min_x, max_x, min_y, max_y)), "Not all bounding points were set" 
		map_.min_bounding_point = Point(min_x, min_y)
		map_.max_bounding_point = Point(max_x, max_y)
		return map_
					
	def get_next_direction(self):
		return next(self.direction_cycle)
		
	def get_destination_coordinates(self, coords, direction):
		assert isinstance(direction, Directions), \
			"Direction must be a member of Directions, not {}".format(direction.__class__.__name__)
		assert direction & (Directions.N | Directions.S) != Directions.N | Directions.S, \
			"Cannot move north and south simultaneously"
		assert direction & (Directions.E | Directions.W) != Directions.E | Directions.W, \
			"Cannot move east and west simultaneously"
		x, y = coords.x, coords.y
		if direction & Directions.N:
			y -= 1
		elif direction & Directions.S:
			y += 1
		if direction & Directions.E:
			x += 1
		elif direction & Directions.W:
			x -= 1
		if x >= len(self.rows[0]):
			self.add_padding(Directions.E)
		if y >= len(self.rows):
			self.add_padding(Directions.S)
		assert x >= 0, "Out of bounds on east/west axis"
		assert y >= 0, "Out of bounds on north/south axis"
		return Point(x, y)
		
	def add_padding(self, direction):
		assert direction is Directions.S or direction is Directions.E, \
			"Cannot add padding in north or west"
		if direction is Directions.S:
			self.rows.append([None] * len(self.rows[0]))
		else:
			for row in self.rows:
				row.append(None)
	
	def is_occupied(self, coords, vector=None):
		if self[coords] is not None:
			return True
		if vector is not None:
			if vector & (Directions.N | Directions.S):
				other_directions = (Directions.E, Directions.W)
			else:
				other_directions = (Directions.N, Directions.S)
			for direction in other_directions:
				if self.is_occupied(self.get_destination_coordinates(coords, direction)):
					return True
		return False
		
	def move(self, occupant, new_coords):
		assert not self.is_occupied(new_coords), f'{new_coords} already occupied'
		self[occupant.coords] = None
		self[new_coords] = occupant
		occupant.coords = new_coords
		if new_coords.x < self.min_bounding_point.x:
			self.min_bounding_point.x = new_coords.x
		elif new_coords.x > self.max_bounding_point.x:
			self.max_bounding_point.x = new_coords.x
		if new_coords.y < self.min_bounding_point.y:
			self.min_bounding_point.y = new_coords.y
		elif new_coords.y > self.max_bounding_point.y:
			self.max_bounding_point.y = new_coords.y
		
	def do_round(self):
		self.current_start_direction = next(self.direction_cycle)
		proposals = {}
		for occupant in self.occupants:
			proposal = occupant.propose_move()
			if proposal:
				try:
					proposals[proposal].append(occupant)
				except KeyError:
					proposals[proposal] = [occupant]
		moves = 0
		for new_coords, accepted_proponents in filter(
			lambda pair: len(pair[1]) == 1, proposals.items()
		):
			self.move(accepted_proponents[0], new_coords)
			moves += 1
		if moves:
			for y_idx in range(self.min_bounding_point.y, len(self.rows)):
				if any(self.rows[y_idx]):
					self.min_bounding_point.y = y_idx
					break
			for y_idx in range(self.max_bounding_point.y, -1, -1):
				if any(self.rows[y_idx]):
					self.max_bounding_point.y = y_idx
					break
			for x_idx in range(self.min_bounding_point.x, len(self.rows[0])):
				if any(row[x_idx] for row in self.rows):
					self.min_bounding_point.x = x_idx
					break
			for x_idx in range(self.max_bounding_point.x, -1, -1):
				if any(row[x_idx] for row in self.rows):
					self.max_bounding_point.x = x_idx
					break
		return moves
		
	@property
	def current_directions_order(self):
		idx = self.directions_order.index(self.current_start_direction)
		return self.directions_order[idx:] + self.directions_order[:idx]
		
	@property
	def empty_spaces_within_min_bounding_rectangle(self):
		spaces = 0
		for row in self.rows[self.min_bounding_point.y:self.max_bounding_point.y+1]:
			spaces += len(list(filter(
				lambda cell: cell is None,
				row[self.min_bounding_point.x:self.max_bounding_point.x+1]
			)))
		return spaces