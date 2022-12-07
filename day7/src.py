class BaseFilesystemObject:
	def __init__(self, name, parent):
		self.name = name
		if parent is None:
			assert name == "/", "The parent may only be None for the root directory"
		else:
			assert isinstance(parent, Directory), "Parent must be a directory"
		self.parent = parent
		
	def __int__(self):
		raise NotImplementedError("Subclasses must implement this method")
		
	def __add__(self, other):
		return int(self) + int(other)
		
	def __radd__(self, other):
		return int(self) + other
		
	def __str__(self):
		if self.parent is None:
			return self.name
		name = str(self.parent)
		if name[-1] != "/":
			name += "/"
		return name + self.name
		
class Directory(BaseFilesystemObject):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.children = {}
		self.total_size = None
		
	def __int__(self):
		if self.total_size is None:
			if self.children:
				self.total_size = sum(self.children.values())
			else:
				self.total_size = 0
		return self.total_size
		
	def __iter__(self):
		for entry in self.children.values():
			yield entry
			if isinstance(entry, Directory):
				yield from entry
		
	def __getitem__(self, key):
		return self.children[key]
		
	def set(self, value):
		assert isinstance(value, BaseFilesystemObject), \
			"Expected BaseFilesystemObject instance, not {}".format(value.__class__.__name__)
		self.children[value.name] = value
		self.total_size = None
		
class File(BaseFilesystemObject):
	def __init__(self, name, parent, size):
		super().__init__(name, parent)
		assert isinstance(size, int) and size >= 0, \
			"File sizes must be positive integers"
		self.size = size
		
	def __int__(self):
		return self.size
	
FILESYSTEM_ROOT = Directory("/", None)
		
class FileSystem:
	UP_ONE_LEVEL = ".."
	
	def __init__(self, total_size=0):
		self.total_size = total_size
		self.cwd = self.root = FILESYSTEM_ROOT
	
	def __int__(self):
		return int(self.root)
		
	def __iter__(self):
		yield from self.root
		
	@property
	def free_space(self):
		return self.total_size - int(self)
		
	def cd(self, to_dir):
		assert ' ' not in to_dir, "Directory names may not contain spaces"
		if to_dir == str(self.root):
			self.cwd = self.root
		elif to_dir == self.UP_ONE_LEVEL:
			if self.cwd is not self.root:
				self.cwd = self.cwd.parent
			else:
				raise RuntimeError("Cannot move one level up from root")
		else:
			self.cwd = self.cwd[to_dir]
			
	def add_entry(self, entry_name, entry_size):
		if entry_size is None:
			entry = Directory(entry_name, self.cwd)
		else:
			entry = File(entry_name, self.cwd, entry_size)
		self.cwd.set(entry)

def read_stream(reader, filesystem_size=0):
	filesystem = FileSystem(filesystem_size)
	for line in reader:
		line = line.strip()
		if line.startswith('$ cd '):
			filesystem.cd(line[5:])
		elif line and not line.startswith('$'):
			disposition, _, name = line.partition(' ')
			if disposition == 'dir':
				size = None
			else:
				size = int(disposition)
			filesystem.add_entry(name, size)
	return filesystem