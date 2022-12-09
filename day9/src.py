from enum import Enum

class Direction(Enum):
	UP = "U"
	DOWN = "D"
	LEFT = "L"
	RIGHT = "R"

class Knot:
	def __init__(self, rope, x, y, idx):
		self.rope = rope
		self.x = x
		self.y = y
		self.idx = idx
		self.next_knot = None
		self.history = []
		self.log_history()
			
	def __str__(self):
		return "({}, {})".format(self.x, self.y)
		
	def __sub__(self, other):
		if not isinstance(other, self.__class__):
			raise NotImplementedError()
		return (self.x - other.x, self.y - other.y)
			
	def move(self, x_offset, y_offset):
		self.x += x_offset
		self.y += y_offset
		self.log_history()
		if self.next_knot:
			(x_diff, y_diff) = self - self.next_knot
			assert abs(x_diff) <= 2 and abs(y_diff) <= 2, \
				"Unexpectedly large move. Current knot positions: {}".format(
					", ".join(str(k) for k in self.rope.head.as_list())
				)
			x_offset, y_offset = 0, 0
			if abs(x_diff) == 2:
				x_offset = -1 if x_diff < 0 else 1
				if abs(y_diff) == 1:
					y_offset = y_diff
			if abs(y_diff) == 2:
				y_offset = -1 if y_diff < 0 else 1
				if abs(x_diff) == 1:
					x_offset = x_diff
			self.next_knot.move(x_offset, y_offset)
		
	def log_history(self):
		self.history.append((self.x, self.y))
		
	def as_list(self):
		list_ = [self]
		while list_[-1].next_knot:
			list_.append(list_[-1].next_knot)
		return list_
		
	@property
	def positions_visited(self):
		return len(set(self.history))

class Rope:
	def __init__(self, total_knots):
		self.head = Knot(self, 0, 0, 0)
		previous = self.head
		for i in range(total_knots - 1):
			knot = Knot(self, 0, 0, i + 1)
			previous.next_knot = knot
			if i == total_knots - 2:
				self.tail = knot
			else:
				previous = knot
		
	def move_head(self, direction, offset):
		if direction is Direction.UP or direction is Direction.DOWN:
			horizontal = False
			mult = -1 if direction is Direction.DOWN else 1
		else:
			horizontal = True
			mult = -1 if direction is Direction.LEFT else 1
		for i in range(abs(offset)):
			if horizontal:
				move = (1 * mult, 0)
			else:
				move = (0, 1 * mult)
			self.head.move(*move)
			
	def read_moves_from_stream(self, stream):
		for line in stream:
			direction, _, offset = line.strip().partition(' ')
			self.move_head(Direction(direction), int(offset))
