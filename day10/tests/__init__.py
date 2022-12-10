import unittest
from io import StringIO
from ..src import CPU

class CPUTest(unittest.TestCase):
	INPUT_1 = """noop
addx 3
addx -5"""

	INPUT_2 = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""
	
	def test_core_behavior(self):
		cpu = CPU(StringIO(self.INPUT_1))
		ticks = []
		values = []
		for tick in cpu:
			ticks.append(tick)
			values.append(cpu.x)
		self.assertEqual(values, [1, 1, 1, 4, 4])
		self.assertEqual(cpu.x, -1)
		self.assertEqual(ticks, list(range(1, 6)))
		
	def test_signal_strength(self):
		cpu = CPU(StringIO(self.INPUT_2))
		strengths = []
		check_at_cycle = 20
		for tick in cpu:
			if tick == check_at_cycle:
				strengths.append(cpu.get_signal_strength())
				check_at_cycle += 40
		self.assertEqual(strengths, [420, 1140, 1800, 2940, 2880, 3960])
		
	def test_draw(self):
		output = StringIO()
		cpu = CPU(StringIO(self.INPUT_2), output)
		cpu.run()
		self.assertEqual(output.getvalue(), """##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######.....""")
	