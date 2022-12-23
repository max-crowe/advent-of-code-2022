import unittest
from ..src import EncryptedList, WraparoundList

class WraparoundListTest(unittest.TestCase):
	def test_wraparound_list(self):
		wraparound = WraparoundList(['foo', 'bar', 'baz'])
		self.assertEqual(wraparound[0], 'foo')
		self.assertEqual(wraparound[1], 'bar')
		self.assertEqual(wraparound[2], 'baz')
		self.assertEqual(wraparound[3], 'foo')
		self.assertEqual(wraparound[7], 'bar')
		self.assertEqual(wraparound[-1], 'baz')
		self.assertEqual(wraparound[-3], 'foo')
		self.assertEqual(wraparound[-4], 'baz')
		self.assertEqual(wraparound[-8], 'bar')

class EncryptedListTest(unittest.TestCase):
	TEST_INPUT = """1
2
-3
3
-2
0
4"""
	DECRYPTION_KEY = 811589153
		
	def test_moves(self):
		test_list = EncryptedList(self.TEST_INPUT.split('\n'))
		expected = [
			[2, 1, -3, 3, -2, 0, 4],
			[1, -3, 2, 3, -2, 0, 4],
			[1, 2, 3, -2, -3, 0, 4],
			[1, 2, -2, -3, 0, 3, 4],
			[1, 2, -3, 0, 3, 4, -2],
			[1, 2, -3, 0, 3, 4, -2],
			[1, 2, -3, 4, 0, 3, -2]
		]
		for step, item in enumerate(test_list.initial, 1):
			test_list.move_item(item)
			expected_list = expected.pop(0)
			self.assertEqual(
				test_list.as_list(),
				expected_list,
				msg=f'List comparison failed on move {step}'
			)
			self.assertEqual(
				test_list.as_list(reverse=True),
				list(reversed(expected_list)),
				msg=f'Reverse list comparison failed on move {step}'
			)
		
	def test_decryption(self):
		test_list = EncryptedList(self.TEST_INPUT.split('\n'))
		mixed = test_list.mix()
		self.assertEqual(mixed, [1, 2, -3, 4, 0, 3, -2])
		base_index = mixed.index(0)
		self.assertEqual(
			mixed[base_index + 1000] + \
			mixed[base_index + 2000] + mixed[base_index + 3000],
			3
		)
		test_list = EncryptedList([3, 1, 0])
		mixed = test_list.mix()
		base_index = mixed.index(0)
		self.assertEqual(
			mixed[base_index + 1000] + \
			mixed[base_index + 2000] + mixed[base_index + 3000],
			4
		)
		
	def test_decryption_with_key(self):
		test_list = EncryptedList(self.TEST_INPUT.split('\n'), self.DECRYPTION_KEY)
		mixed = test_list.mix(rounds=10)
		base_index = mixed.index(0)
		self.assertEqual(
			mixed,
			[0, -2434767459, 1623178306, 3246356612, -1623178306, 2434767459, 811589153]
		)
		self.assertEqual(
			mixed[base_index + 1000] + \
			mixed[base_index + 2000] + mixed[base_index + 3000],
			1623178306
		)
