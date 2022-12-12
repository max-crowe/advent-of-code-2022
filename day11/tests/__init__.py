import math, unittest
from functools import reduce
from io import StringIO
from ..src import Scheduler

class MonkeyTest(unittest.TestCase):
    TEST_INPUT = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""
    
    def test_standard_worry_handler(self):
        scheduler = Scheduler.read_input(StringIO(self.TEST_INPUT), lambda v: v // 3)
        self.assertEqual(len(scheduler.monkeys), 4)
        # Round 1
        scheduler.do_round()
        self.assertEqual(
            list(scheduler.monkeys[0]),
            [20, 23, 27, 26]
        )
        self.assertEqual(
            list(scheduler.monkeys[1]),
            [2080, 25, 167, 207, 401, 1046]
        )
        self.assertEqual(
            list(scheduler.monkeys[2]),
            []
        )
        self.assertEqual(
            list(scheduler.monkeys[3]),
            []
        )
        # Round 2
        scheduler.do_round()
        self.assertEqual(
            list(scheduler.monkeys[0]),
            [695, 10, 71, 135, 350]
        )
        self.assertEqual(
            list(scheduler.monkeys[1]),
            [43, 49, 58, 55, 362]
        )
        self.assertEqual(
            list(scheduler.monkeys[2]),
            []
        )
        self.assertEqual(
            list(scheduler.monkeys[3]),
            []
        )
        # Round 3
        scheduler.do_round()
        self.assertEqual(
            list(scheduler.monkeys[0]),
            [16, 18, 21, 20, 122]
        )
        self.assertEqual(
            list(scheduler.monkeys[1]),
            [1468, 22, 150, 286, 739]
        )
        self.assertEqual(
            list(scheduler.monkeys[2]),
            []
        )
        self.assertEqual(
            list(scheduler.monkeys[3]),
            []
        )
        # Round 4
        scheduler.do_round()
        self.assertEqual(
            list(scheduler.monkeys[0]),
            [491, 9, 52, 97, 248, 34]
        )
        self.assertEqual(
            list(scheduler.monkeys[1]),
            [39, 45, 43, 258]
        )
        self.assertEqual(
            list(scheduler.monkeys[2]),
            []
        )
        self.assertEqual(
            list(scheduler.monkeys[3]),
            []
        )
        # Round 5
        scheduler.do_round()
        self.assertEqual(
            list(scheduler.monkeys[0]),
            [15, 17, 16, 88, 1037]
        )
        self.assertEqual(
            list(scheduler.monkeys[1]),
            [20, 110, 205, 524, 72]
        )
        self.assertEqual(
            list(scheduler.monkeys[2]),
            []
        )
        self.assertEqual(
            list(scheduler.monkeys[3]),
            []
        )
        for i in range(15):
            scheduler.do_round()
        self.assertEqual(scheduler.monkeys[0].items_inspected, 101)
        self.assertEqual(scheduler.monkeys[1].items_inspected, 95)
        self.assertEqual(scheduler.monkeys[2].items_inspected, 7)
        self.assertEqual(scheduler.monkeys[3].items_inspected, 105)
        
    def test_extra_worry_handler(self):
    	scheduler = Scheduler.read_input(StringIO(self.TEST_INPUT))
    	scheduler.discard_handler = lambda v: v % reduce(lambda x, y: x * y, [m.divisor for m in scheduler.monkeys])
    	expected_results = [
    		[2, 4, 3, 6],
    		[99, 97, 8, 103],
    		[5204, 4792, 199, 5192],
    		[52166, 47830, 1938, 52013]
    	]
    	absolute_maximum = max(max(expected) for expected in expected_results)
    	actual_results = []
    	sample_at = {1, 20, 1000, 10000}
    	for i in range(10000):
    		scheduler.do_round()
    		current_maximum = max(max(m.current_items) if m.current_items else 0 for m in scheduler.monkeys)
    		if i + 1 in sample_at:
    			actual_results.append([m.items_inspected for m in scheduler.monkeys])
	    		self.assertEqual(actual_results, expected_results[:len(actual_results)])
    	