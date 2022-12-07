#!/usr/bin/env python
import sys

def split_contents(contents):
	midpoint = int(len(contents) / 2)
	return contents[0:midpoint], contents[midpoint:]
	
def get_priority(item):
	ord_item = ord(item)
	if ord_item >= 97:
		return ord_item - 96
	return ord_item - 38
	
def get_common_items(contents):
	first_half, second_half = split_contents(contents)
	return set(c for c in first_half) & set(c for c in second_half)
	
def handle_buffer(buffer):
	common_item = set(c for c in buffer[0]) & set(c for c in buffer[1]) & set(c for c in buffer[2])
	assert len(common_item) == 1
	return get_priority(list(common_item)[0])
	
if __name__ == '__main__':
	p_sum = 0
	buffer = []
	buffer_len = 0
	with open(sys.argv[1]) as input_data:
		for line in input_data:
			"""
			for common_item in get_common_items(line.strip()):
				print((get_priority(common_item), common_item))
				p_sum += get_priority(common_item)
			"""
			if buffer_len == 3:	
				p_sum += handle_buffer(buffer)
				buffer = []
				buffer_len = 0
			buffer.append(line.strip())
			buffer_len += 1
	if buffer:
		p_sum += handle_buffer(buffer)
	print(p_sum)