#!/usr/bin/env python
import sys
from argparse import ArgumentParser
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.resolve()))
from day20.src import EncryptedList

if __name__ == "__main__":
	parser = ArgumentParser()
	parser.add_argument('input', type=lambda p: open(p).read().split('\n'))
	parser.add_argument('--paranoid', action='store_true')
	parser.add_argument('--key', type=int)
	parser.add_argument('--rounds', type=int, default=1)
	args = parser.parse_args()
	encrypted = EncryptedList(args.input, decryption_key=args.key, paranoid=args.paranoid)
	mixed = encrypted.mix(args.rounds)
	base_index = mixed.index(0)
	print(mixed[base_index + 1000] + mixed[base_index + 2000] + mixed[base_index + 3000])