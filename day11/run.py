#!/usr/bin/env python
import sys
from argparse import ArgumentParser
from functools import reduce
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.resolve()))
from day11.src import Scheduler

if __name__ == "__main__":
	parser = ArgumentParser()
	parser.add_argument('input', type=lambda i: open(i))
	parser.add_argument('rounds', type=int)
	parser.add_argument('--use-alternate-worry-handler', action="store_true")
	args = parser.parse_args()
	scheduler = Scheduler.read_input(args.input)
	if args.use_alternate_worry_handler:
		scheduler.discard_handler = lambda v: v % reduce(lambda x, y: x * y, [m.divisor for m in scheduler.monkeys])
	else:
		scheduler.discard_handler = lambda v: v // 3
	for i in range(args.rounds):
		scheduler.do_round()
	most_active_monkeys = sorted(scheduler.monkeys, key=lambda m: m.items_inspected, reverse=True)
	print("Most active: {}, least active: {}".format(
		most_active_monkeys[0].items_inspected,
		most_active_monkeys[-1].items_inspected
	))
	print("Monkey business: {}".format(
		most_active_monkeys[0].items_inspected * most_active_monkeys[1].items_inspected
	))
