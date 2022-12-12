import operator, re
from collections import deque
from math import floor

class Monkey:
	def __init__(
		self,
		scheduler,
		starting_items,
		inspect_operation,
		divisor,
		target_if_true,
		target_if_false
	):
		assert all(isinstance(item, int) for item in starting_items), \
			"Items must be passed as a list of integers"
		assert callable(inspect_operation), "The operation must be a callable"
		assert isinstance(target_if_true, (MonkeyPromise, self.__class__)) and isinstance(
			target_if_false, (MonkeyPromise, self.__class__)
		), "Unexpected target type {}".format(self.__class__)
		self.scheduler = scheduler
		self.current_items = deque(starting_items)
		self.inspect_operation = inspect_operation
		self.divisor = divisor
		self.items_inspected = 0
		self.targets = [target_if_false, target_if_true]
		
	def __iter__(self):
		yield from self.current_items
		
	def inspect(self):
		self.current_items[0] = self.inspect_operation(self.current_items[0])
		#print("Value before discard: {}".format(self.current_items[0]))
		self.current_items[0] = self.scheduler.discard_handler(self.current_items[0])
		self.items_inspected += 1
		
	def throw(self):
		target = int(self.current_items[0] % self.divisor == 0)
		self.targets[target].current_items.append(
			self.current_items.popleft()
		)
		
	def do_turn(self):
		while self.current_items:
			self.inspect()
			self.throw()
		
class MonkeyPromise:
	def __init__(self, monkey_list, idx):
		self.monkey_list = monkey_list
		self.idx = idx
		self.monkey = None
		
	def __getattr__(self, name):
		if self.monkey is None:
			self.monkey = self.monkey_list[self.idx]
		return getattr(self.monkey, name)
		
class Scheduler:
	OPERATORS = {
		'+': operator.add,
		'*': operator.mul
	}
	ITEMS_PATTERN = re.compile(r'items: ([ ,0-9]+)$')
	OPERATION_PATTERN = re.compile(r'old ([{}]) (\d+|old)$'.format(''.join(OPERATORS.keys())))
	TAIL_NUMBER_PATTERN = re.compile(r' (\d+)$')
	
	def __init__(self, discard_handler=None):
		self.monkeys = []
		self.discard_handler = discard_handler
		self.current_round = 0
		
	def add_monkey(
		self,
		starting_items,
		inspect_operation,
		divisor,
		target_idx_if_true,
		target_idx_if_false
	):
		self.monkeys.append(Monkey(
			self,
			starting_items,
			inspect_operation,
			divisor,
			MonkeyPromise(self.monkeys, target_idx_if_true),
			MonkeyPromise(self.monkeys, target_idx_if_false)
		))
		
	def do_round(self):
		self.current_round += 1
		for i, monkey in enumerate(self.monkeys):
			monkey.do_turn()
			
	@classmethod
	def make_operation(cls, op, operand):
		operation = cls.OPERATORS[op]
		if operand == "old":
			return lambda v: operation(v, v)
		return lambda v: operation(v, int(operand))
		
	@classmethod
	def make_test(cls, operand):
		return lambda v: v % operand == 0
		
	@classmethod	
	def read_input(cls, input_stream, *args):
		scheduler = cls(*args)
		current_args = None
		for line in input_stream:
			line = line.strip()
			if not line:
				continue
			elif line.startswith("Monkey"):
				if current_args:
					scheduler.add_monkey(*tuple(current_args))
				current_args = []
			else:
				if match := cls.ITEMS_PATTERN.search(line):
					starting_items = match.group(1).split(', ')
					current_args.append([int(v) for v in starting_items])
				elif match := cls.OPERATION_PATTERN.search(line):
					operation = cls.OPERATORS[match.group(1)]
					operand = match.group(2)
					current_args.append(cls.make_operation(
						match.group(1),
						match.group(2)
					))
				else:
					match = cls.TAIL_NUMBER_PATTERN.search(line)
					operand = int(match.group(1))
					current_args.append(operand)
		scheduler.add_monkey(*tuple(current_args))
		return scheduler
		