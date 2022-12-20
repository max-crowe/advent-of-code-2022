class Node:
	def __init__(self, map_, chr, x, y):
		self.map = map_
		self.x = x
		self.y = y
		chr_code = ord(chr)
		assert 97 <= chr_code <= 122, "Invalid height designation"
		self.height = chr_code - 97
		self.accessible_neighbors = set()
		self.shortest_paths = None
		
	def __str__(self):
		return f'({self.x}, {self.y})'
		
	def __repr__(self):
		return str(self)
		
	def __eq__(self, other):
		return (self.x, self.y) == (other.x, other.y)
		
	def __hash__(self):
		return hash((self.x, self.y))
		
	def add_neighbor(self, neighbor):
		if neighbor.height - self.height <= 1:
			self.accessible_neighbors.add(neighbor)
		
	def get_shortest_path(self, destination):
		self.shortest_paths = {self: []}
		visited = set()
		current_node = self
		while current_node:
			for neighbor in current_node.accessible_neighbors:
				tentative_path = self.shortest_paths[current_node] + [neighbor]
				try:
					shortest_known_path_length = len(self.shortest_paths[neighbor])
				except KeyError:
					shortest_known_path_length = None
				if shortest_known_path_length is None or len(tentative_path) < shortest_known_path_length:
					self.shortest_paths[neighbor] = tentative_path
				if neighbor is destination:
					return tentative_path
			visited.add(current_node)
			next_node = None
			for unvisited_node in visited ^ set(self.shortest_paths.keys()):
				if next_node is None or len(self.shortest_paths[unvisited_node]) < len(self.shortest_paths[next_node]):
					next_node = unvisited_node
			current_node = next_node
		
class Map:
	def __init__(self):
		self.origin = None
		self.destination = None
		self.nodes = set()
		
	@classmethod
	def read_input_with_grid(cls, input_stream):
		map_ = cls()
		grid = []
		for row_idx, line in enumerate(input_stream):
			row = []
			grid.append(row)
			for col_idx, char in enumerate(line.strip()):
				if char == 'S':
					map_.origin = node = Node(map_, 'a', col_idx, row_idx)
				elif char == 'E':
					map_.destination = node = Node(map_, 'z', col_idx, row_idx)
				else:
					node = Node(map_, char, col_idx, row_idx)
				row.append(node)
				map_.nodes.add(node)
				if col_idx > 0:
					row[col_idx - 1].add_neighbor(node)
					node.add_neighbor(row[col_idx - 1])
				if row_idx > 0:
					grid[row_idx - 1][col_idx].add_neighbor(node)
					node.add_neighbor(grid[row_idx - 1][col_idx])
		return map_, grid
		
	@classmethod
	def read_input(cls, input_stream):
		return cls.read_input_with_grid(input_stream)[0]
		
	def find_best_path_from_arbitrary_origin(self, filter_criteria):
		best_candidate = None
		for node in filter(filter_criteria, self.nodes):
			shortest_path = node.get_shortest_path(self.destination)
			if shortest_path is None:
				continue
			if best_candidate is None or len(shortest_path) < len(best_candidate):
				best_candidate = shortest_path
		return best_candidate