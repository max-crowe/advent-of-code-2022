#!/usr/bin/env python
import math, sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.resolve()))
from day7.src import read_stream, Directory

def do_binary_search(data, next_highest_value):
	mid = math.floor((len(data) - 1) / 2)
	value = data[mid]
	try:
		next_value = data[mid + 1]
	except IndexError:
		next_value = None
	if value == next_highest_value:
		return value
	if value < next_highest_value:
		if next_value is None:
			raise RuntimeError("No such value")
		if next_value >= next_highest_value:
			return next_value
		return do_binary_search(data[mid+1:], next_highest_value)
	if mid == 0:
		raise RuntimeError("No such value")
	if data[mid - 1] < next_highest_value:
		return value
	return do_binary_search(data[:mid], next_highest_value)

if __name__ == "__main__":
	with open(sys.argv[1]) as stream:
		filesystem = read_stream(stream, 70000000)
	print("Total filesystem size is {}".format(int(filesystem)))
	dir_sizes = sorted(int(entry) for entry in filter(lambda entry: isinstance(entry, Directory), filesystem))
	target_space = 30000000 - filesystem.free_space
	print(f"Target space is {target_space}")
	print(do_binary_search(dir_sizes, target_space))