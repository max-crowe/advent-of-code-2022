#!/usr/bin/env python
import re, sys
from collections import deque

def init_queues(input_file):
	queues = None
	queue_count = 0
	for line in input_file:
		if line[0] != '[':
			return queues
		if not queues:
			queue_count = int(len(line) / 4)
			queues = [deque() for i in range(queue_count)]
		for i in range(queue_count):
			char = line[(i * 4) + 1]
			if char != ' ':
				assert 65 <= ord(char) <= 90
				queues[i].appendleft(char)
				
def move_crates(input_file, queues, lifo=True):
	moves = 0
	for line in input_file:
		match = re.match(r'move ([0-9]+) from ([0-9]+) to ([0-9]+)$', line)
		if not match:
			continue
		moves += 1
		move_count = int(match.group(1))
		from_queue = int(match.group(2)) - 1
		to_queue = int(match.group(3)) - 1
		if lifo:
			for i in range(move_count):
				queues[to_queue].append(queues[from_queue].pop())
		else:
			moved_crates = deque()
			for i in range(move_count):
				moved_crates.appendleft(queues[from_queue].pop())
			while moved_crates:
				queues[to_queue].append(moved_crates.popleft())
	print(f'Performed {moves} moves')
				
if __name__ == '__main__':
	with open(sys.argv[1]) as input_file:
		queues = init_queues(input_file)
		move_crates(input_file, queues, False)
		print(''.join(queue.pop() for queue in queues))