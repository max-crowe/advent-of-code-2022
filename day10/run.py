#!/usr/bin/env python
import sys
from argparse import ArgumentParser
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.resolve()))
from day10.src import CPU

if __name__ == "__main__":
	parser = ArgumentParser()
	parser.add_argument('program', type=lambda p: open(p))
	parser.add_argument('--draw', action='store_true')
	args = parser.parse_args()
	output = sys.stdout if args.draw else None
	cpu = CPU(args.program, output)
	if args.draw:
		cpu.run()
	else:
		strengths_sum = 0
		check_at_cycle = 20
		for cycle in cpu:
			if cycle == check_at_cycle:
				print("Sampling strength...")
				strengths_sum += cpu.get_signal_strength()
				check_at_cycle += 40
		print(f"Signal strength sum: {strengths_sum}")
	