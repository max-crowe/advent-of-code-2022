#!/usr/bin/env python
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.resolve()))
from day7.src import read_stream, Directory

if __name__ == "__main__":
	with open(sys.argv[1]) as stream:
		filesystem = read_stream(stream)
	print("Total filesystem size is {}".format(int(filesystem)))
	size_sum = 0
	for entry in filter(lambda entry: isinstance(entry, Directory), filesystem):
		entry_size = int(entry)
		if entry_size <= 100000:
			size_sum += entry_size
	print(size_sum)
