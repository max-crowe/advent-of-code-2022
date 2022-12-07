def read_buffer(buf, target_distinct_char_count):
	chars_read = 0
	marker = ''
	marker_size = 0
	marker_distinct_chars = 0
	for char in buf:
		chars_read += 1
		if marker_size == target_distinct_char_count:
			discard = marker[0]
			marker = marker[1:]
			marker_size -= 1
			if discard not in marker:
				marker_distinct_chars -= 1
		if not char in marker:
			marker_distinct_chars += 1
		marker += char
		marker_size += 1
		if marker_size == marker_distinct_chars == target_distinct_char_count:
			return chars_read
	raise ValueError('No marker found')

def find_start_of_packet(buf):
	return read_buffer(buf, 4)
	
def find_start_of_message(buf):
	return read_buffer(buf, 14)
