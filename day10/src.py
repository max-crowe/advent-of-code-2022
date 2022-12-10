from enum import IntEnum

class CPU:
	class Instruction(IntEnum):
		noop = 1
		addx = 2
	
	def __init__(self, program_input, output_stream=None):
		self.x = 1
		self.cycle = 0
		self.sprite_padding = 1
		self.output_stream = output_stream
		self.program_input = iter(program_input)
		
	def __iter__(self):
		while True:
			try:
				instruction, operand = self.read_next_instruction()
				instruction_ticks = int(instruction)
				for i in range(instruction_ticks):
					self.draw()
					self.cycle += 1
					yield self.cycle
					if instruction is self.Instruction.addx and i + 1 == instruction_ticks:
						self.x += operand
			except StopIteration:
				break
				
	def read_next_instruction(self):
		line = next(self.program_input)
		instruction_name, _, operand = line.strip().partition(' ')
		if operand == '':
			operand = None
		else:
			operand = int(operand)
		return self.Instruction[instruction_name], operand
		
	def get_signal_strength(self):
		return self.x * self.cycle
		
	def draw(self):
		if self.output_stream is None:
			return
		draw_pos = self.cycle % 40
		if self.cycle and draw_pos == 0:
			self.output_stream.write('\n')
		if self.x - self.sprite_padding <= draw_pos <= self.x + self.sprite_padding:
			self.output_stream.write('#')
		else:
			self.output_stream.write('.')
			
	def run(self):
		for cycle in self:
			pass
	