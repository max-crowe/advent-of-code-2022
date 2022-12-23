from functools import cached_property

class WraparoundList(list):
	def __getitem__(self, idx):
		is_negative = idx < 0
		if isinstance(idx, int) and (not is_negative and idx >= len(self)) or (
			is_negative and idx * -1 > len(self)
		):
			idx = abs(idx) % len(self)
			if is_negative:
				idx *= -1
		return super().__getitem__(idx)

class ListItem:
	def __init__(self, parent, value, decryption_key=None):
		self.parent = parent
		self.value = int(value)
		if decryption_key:
			self.value *= decryption_key
		self.next_item = None
		self.prev_item = None
		
	def __repr__(self):
		return str(int(self))
		
	def __int__(self):
		return self.value
		
	def link_next(self, other):
		assert other is not self, f"Cannot create circular reference from {self} to itself"
		self.next_item = other
		if other is not None:
			other.prev_item = self
			
	def detach(self):
		if self.prev_item:
			self.prev_item.link_next(self.next_item)
		else:
			self.next_item.prev_item = None
		if self is self.parent.start:
			self.parent.start = self.next_item
		elif self is self.parent.end:
			self.parent.end = self.prev_item
		
	def replace(self, other):
		self_next = self.next_item
		self_prev = self.prev_item
		other_next = other.next_item
		other.link_next(self)
		self.link_next(other_next)
		if self.parent.start is self:
			self.parent.start = self_next
		if other is self.parent.end:
			self.parent.end = self
		elif self is self.parent.end:
			self.parent.end = self_prev
		
class EncryptedList:
	def __init__(self, initial, decryption_key=None, paranoid=False):
		self.initial = []
		self.decryption_key = decryption_key
		self.paranoid = paranoid
		self.start = None
		self.end = None
		for data in initial:
			item = ListItem(self, data, self.decryption_key)
			try:
				self.initial[-1].link_next(item)
			except IndexError:
				pass
			self.initial.append(item)
		self.start = self.initial[0]
		self.end = self.initial[-1]
		self.length = len(self.initial)
		
	def __len__(self):
		return self.length
		
	def get_item_to_replace(self, item):
		moves = abs(int(item)) % (len(self) - 1)
		if int(item) < 0:
			moves += 1
		if not moves:
			return
		item.detach()
		current = item
		for i in range(abs(moves)):
			if int(item) > 0:
				current = current.next_item or self.start
			else:
				current = current.prev_item or self.end
		return current
		
	def move_item(self, item):
		item_to_replace = self.get_item_to_replace(item)
		if item_to_replace:
			item.prev_item = None
			item.next_item = None
			item.replace(item_to_replace)
			
	def as_list(self, reverse=False):
		list_ = []
		if reverse:
			current = self.end
			while current is not None:
				list_.append(int(current))
				current = current.prev_item
		else:
			current = self.start
			while current is not None:
				list_.append(int(current))
				current = current.next_item
		return list_
			
	def mix(self, rounds=1):
		for i in range(rounds):
			for item in self.initial:
				self.move_item(item)
				if self.paranoid:
					as_list = self.as_list()
					as_list_reversed = list(reversed(self.as_list(reverse=True)))
					all_items = []
					current = self.start
					while current is not None:
						all_items.append(current)
						current = current.next_item
					if as_list != as_list_reversed or len(set(all_items)) != len(self.initial):
						raise RuntimeError(
							f"List reversal integrity failure after moving item {item}"
						)
		return WraparoundList(self.as_list())
