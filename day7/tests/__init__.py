from io import StringIO
from unittest import TestCase
from ..src import read_stream

class FileSystemTestCase(TestCase):
	TEST_STREAM = """
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k		
"""
	def get_test_filesystem(self):
		return read_stream(StringIO(self.TEST_STREAM))

	def test_sizes(self):
		filesystem = self.get_test_filesystem()
		self.assertEqual(int(filesystem.root["a"]["e"]), 584)
		self.assertEqual(int(filesystem.root["a"]["f"]), 29116)
		self.assertEqual(int(filesystem.root["a"]["g"]), 2557)
		self.assertEqual(int(filesystem.root["a"]["h.lst"]), 62596)
		self.assertEqual(int(filesystem.root["a"]), 94853)
		self.assertEqual(int(filesystem.root["d"]), 24933642)
		self.assertEqual(int(filesystem), 48381165)
		
	def test_iteration(self):
		filesystem = self.get_test_filesystem()
		contents = [str(entry) for entry in filesystem]
		self.assertEqual(contents, [
			"/a",
			"/a/e",
			"/a/e/i",
			"/a/f",
			"/a/g",
			"/a/h.lst",
			"/b.txt",
			"/c.dat",
			"/d",
			"/d/j",
			"/d/d.log",
			"/d/d.ext",
			"/d/k"
		])
	