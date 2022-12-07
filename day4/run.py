#!/usr/bin/env python
import sys

def get_bounds(pair):
	start, _, end = pair.partition('-')
	start = int(start)
	end = int(end)
	assert start <= end, f'{start} is not less than {end}'
	return start, end

def iter_input(path):
	with open(path) as input_file:
		for line in input_file:
			pair1, _, pair2 = line.strip().partition(',')
			pair1_start, pair1_end = get_bounds(pair1)
			pair2_start, pair2_end = get_bounds(pair2)
			yield (pair1_start, pair1_end), (pair2_start, pair2_end)
			
def overlaps_full(pair1_bounds, pair2_bounds):
	return (pair1_bounds[0] <= pair2_bounds[0] and pair1_bounds[1] >= pair2_bounds[1]) or (
		pair1_bounds[0] >= pair2_bounds[0] and pair1_bounds[1] <= pair2_bounds[1]
	)
	
def overlaps_any(pair1_bounds, pair2_bounds):
	return (pair2_bounds[0] <= pair1_bounds[0] <= pair2_bounds[1]) or (
		pair1_bounds[0] <= pair2_bounds[0] <= pair1_bounds[1]
	)
			
def find_full_overlaps(path):
	overlaps = 0
	for pair1_bounds, pair2_bounds in iter_input(path):
		if overlaps_full(pair1_bounds, pair2_bounds):
			overlaps += 1
	return overlaps
	
def find_any_overlaps(path):
	overlaps = 0
	for pair1_bounds, pair2_bounds in iter_input(path):
		if overlaps_any(pair1_bounds, pair2_bounds):
			overlaps += 1
			if not overlaps_full(pair1_bounds, pair2_bounds):
				print(pair1_bounds, pair2_bounds)
	return overlaps
			
if __name__ == '__main__':
	print(find_any_overlaps(sys.argv[1]))