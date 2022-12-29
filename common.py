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
		
class BaseMap:
	def __init__(self):
		self.rows = []
		
	def __getitem__(self, coords):
		return self.rows[coords.y][coords.x]
		
	def __setitem__(self, coords, item):
		self.rows[coords.y][coords.x] = item