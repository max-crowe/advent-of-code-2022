from unittest import TestCase
from ..src import find_start_of_message, find_start_of_packet

class BufferReaderTestCase(TestCase):
	def test_find_start_of_packet(self):
		self.assertEqual(
			find_start_of_packet('bvwbjplbgvbhsrlpgdmjqwftvncz'), 5
		)
		self.assertEqual(
			find_start_of_packet('nppdvjthqldpwncqszvftbrmjlhg'), 6
		)
		self.assertEqual(
			find_start_of_packet('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg'), 10
		)
		self.assertEqual(
			find_start_of_packet('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw'), 11
		)
		self.assertEqual(
			find_start_of_packet('xpqrosimcpoosjguip'), 4
		)
		self.assertEqual(
			find_start_of_packet('aabcdefg'), 5
		)
		test_str = 'ababababababababcd'
		self.assertEqual(
			find_start_of_packet(test_str), len(test_str)
		)
		with self.assertRaises(ValueError):
			find_start_of_packet('aabbccddeeffgghhiijjkkllmmnnoop')
			
	def test_find_start_of_message(self):
		self.assertEqual(
			find_start_of_message('mjqjpqmgbljsphdztnvjfqwrcgsmlb'), 19
		)
		self.assertEqual(
			find_start_of_message('bvwbjplbgvbhsrlpgdmjqwftvncz'), 23
		)
		self.assertEqual(
			find_start_of_message('nppdvjthqldpwncqszvftbrmjlhg'), 23
		)
		self.assertEqual(
			find_start_of_message('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg'), 29
		)
		self.assertEqual(
			find_start_of_message('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw'), 26
		)
	