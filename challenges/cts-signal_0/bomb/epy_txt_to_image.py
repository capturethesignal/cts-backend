"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
from PIL import Image, ImageDraw, ImageFont


class blk(gr.basic_block):  # sync_block):
	"""Text to Image"""

	# only default arguments here
	def __init__(self, image_file_name="", image_width=0, message_font="", message_text=""):
		"""arguments to this function show up as parameters in GRC"""
		gr.basic_block.__init__(
			self,
			name='Text to Image',   # will show up in GRC
			in_sig=[],
			out_sig=[])
		# if an attribute with the same name as a parameter is found, a callback is registered (properties work, too).
		self.image_file_name = image_file_name
		self.image_width = image_width
		self.message_font = message_font
		self.message_text = message_text
		if self.image_file_name != "":
			self.create_image()
		return

	def create_image(self):
		size = 1
		while(True):
			font = ImageFont.truetype(self.message_font, size)
			length, width = font.getsize(self.message_text)
			if width > self.image_width:
				size = size - 1
				font = ImageFont.truetype(self.message_font, size)
				length, width = font.getsize(self.message_text)
				extra_length, _ = font.getsize("XX")
				length += extra_length
				break
			size += 1

		# print self.image_file_name, length, width, size

		img = Image.new('RGB', (length, self.image_width), color=(0, 0, 0))
		d = ImageDraw.Draw(img)
		d.text((0, 0), self.message_text, font=font, fill=(255, 255, 255))
		transposed = img
		transposed = transposed.transpose(Image.ROTATE_90)
		transposed = transposed.transpose(Image.FLIP_TOP_BOTTOM)
		transposed.save(self.image_file_name)
		return

	# def work(self, input_items, output_items):
	#    output_items[0][:] = input_items[0]
	#    return len(output_items[0])
