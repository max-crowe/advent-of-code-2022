#!/usr/bin/env python
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.resolve()))
from day6.src import find_start_of_message, find_start_of_packet

if __name__ == '__main__':
	with open(sys.argv[1]) as input_file:
		#print(find_start_of_packet(input_file.read()))
		print(find_start_of_message(input_file.read()))