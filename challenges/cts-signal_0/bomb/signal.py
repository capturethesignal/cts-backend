#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: signal
# Author: Jonathan Andersson
# GNU Radio version: 3.7.14.0
##################################################

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from offset_tx import offset_tx  # grc-generated hier_block
from optparse import OptionParser
import ConfigParser
import epy_chdir  # embedded python module
import epy_txt_to_image
import paint


class signal(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "signal")

        ##################################################
        # Variables
        ##################################################
        self.signal_name = signal_name = "signal"
        self.config_file = config_file = "signal.cfg"
        self._tx_frequency_config = ConfigParser.ConfigParser()
        self._tx_frequency_config.read(config_file)
        try: tx_frequency = self._tx_frequency_config.getint(signal_name, "tx_frequency")
        except: tx_frequency = 400000000
        self.tx_frequency = tx_frequency
        self._tune_offset_config = ConfigParser.ConfigParser()
        self._tune_offset_config.read(config_file)
        try: tune_offset = self._tune_offset_config.getint(signal_name, "tune_offset")
        except: tune_offset = 19000
        self.tune_offset = tune_offset
        self._samp_rate_config = ConfigParser.ConfigParser()
        self._samp_rate_config.read(config_file)
        try: samp_rate = self._samp_rate_config.getint(signal_name, "samp_rate")
        except: samp_rate = 0
        self.samp_rate = samp_rate
        self._ota_config = ConfigParser.ConfigParser()
        self._ota_config.read(config_file)
        try: ota = self._ota_config.get(signal_name, "ota")
        except: ota = 'False'
        self.ota = ota
        self._message_text_config = ConfigParser.ConfigParser()
        self._message_text_config.read(config_file)
        try: message_text = self._message_text_config.get(signal_name, "message_text")
        except: message_text = ''
        self.message_text = message_text
        self._message_font_config = ConfigParser.ConfigParser()
        self._message_font_config.read(config_file)
        try: message_font = self._message_font_config.get(signal_name, "message_font")
        except: message_font = ''
        self.message_font = message_font
        self._image_width_config = ConfigParser.ConfigParser()
        self._image_width_config.read(config_file)
        try: image_width = self._image_width_config.getint(signal_name, "image_width")
        except: image_width = 0
        self.image_width = image_width
        self._image_line_repeat_config = ConfigParser.ConfigParser()
        self._image_line_repeat_config.read(config_file)
        try: image_line_repeat = self._image_line_repeat_config.getint(signal_name, "image_line_repeat")
        except: image_line_repeat = 0
        self.image_line_repeat = image_line_repeat
        self._image_file_name_config = ConfigParser.ConfigParser()
        self._image_file_name_config.read(config_file)
        try: image_file_name = self._image_file_name_config.get(signal_name, "image_file_name")
        except: image_file_name = ''
        self.image_file_name = image_file_name
        self._device_string_config = ConfigParser.ConfigParser()
        self._device_string_config.read(config_file)
        try: device_string = self._device_string_config.get('main', "device_string")
        except: device_string = 'bladerf=0,verbosity=debug,xb200=custom'
        self.device_string = device_string

        ##################################################
        # Blocks
        ##################################################
        self.paint_paint_bc_0 = paint.paint_bc(image_width, image_line_repeat, paint.EQUALIZATION_OFF, paint.INTERNAL, 1)
        self.paint_image_source_0 = paint.image_source(image_file_name, 0, 0, 0, 0, 2)
        self.offset_tx_0 = offset_tx(
            config_file=config_file,
            device_string=device_string,
            ota=ota,
            samp_rate=samp_rate,
            tune_offset=tune_offset,
            tx_frequency=tx_frequency,
        )
        self.epy_txt_to_image = epy_txt_to_image.blk(image_file_name=image_file_name, image_width=image_width, message_font=message_font, message_text=message_text)
        self.blocks_tag_gate_0 = blocks.tag_gate(gr.sizeof_gr_complex * 1, False)
        self.blocks_tag_gate_0.set_single_key("")



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_tag_gate_0, 0), (self.offset_tx_0, 0))
        self.connect((self.paint_image_source_0, 0), (self.paint_paint_bc_0, 0))
        self.connect((self.paint_paint_bc_0, 0), (self.blocks_tag_gate_0, 0))

    def get_signal_name(self):
        return self.signal_name

    def set_signal_name(self, signal_name):
        self.signal_name = signal_name
        self._tx_frequency_config = ConfigParser.ConfigParser()
        self._tx_frequency_config.read(self.config_file)
        if not self._tx_frequency_config.has_section(self.signal_name):
        	self._tx_frequency_config.add_section(self.signal_name)
        self._tx_frequency_config.set(self.signal_name, "tx_frequency", str(None))
        self._tx_frequency_config.write(open(self.config_file, 'w'))
        self._tune_offset_config = ConfigParser.ConfigParser()
        self._tune_offset_config.read(self.config_file)
        if not self._tune_offset_config.has_section(self.signal_name):
        	self._tune_offset_config.add_section(self.signal_name)
        self._tune_offset_config.set(self.signal_name, "tune_offset", str(None))
        self._tune_offset_config.write(open(self.config_file, 'w'))
        self._samp_rate_config = ConfigParser.ConfigParser()
        self._samp_rate_config.read(self.config_file)
        if not self._samp_rate_config.has_section(self.signal_name):
        	self._samp_rate_config.add_section(self.signal_name)
        self._samp_rate_config.set(self.signal_name, "samp_rate", str(None))
        self._samp_rate_config.write(open(self.config_file, 'w'))
        self._ota_config = ConfigParser.ConfigParser()
        self._ota_config.read(self.config_file)
        if not self._ota_config.has_section(self.signal_name):
        	self._ota_config.add_section(self.signal_name)
        self._ota_config.set(self.signal_name, "ota", str(None))
        self._ota_config.write(open(self.config_file, 'w'))
        self._message_text_config = ConfigParser.ConfigParser()
        self._message_text_config.read(self.config_file)
        if not self._message_text_config.has_section(self.signal_name):
        	self._message_text_config.add_section(self.signal_name)
        self._message_text_config.set(self.signal_name, "message_text", str(None))
        self._message_text_config.write(open(self.config_file, 'w'))
        self._message_font_config = ConfigParser.ConfigParser()
        self._message_font_config.read(self.config_file)
        if not self._message_font_config.has_section(self.signal_name):
        	self._message_font_config.add_section(self.signal_name)
        self._message_font_config.set(self.signal_name, "message_font", str(None))
        self._message_font_config.write(open(self.config_file, 'w'))
        self._image_width_config = ConfigParser.ConfigParser()
        self._image_width_config.read(self.config_file)
        if not self._image_width_config.has_section(self.signal_name):
        	self._image_width_config.add_section(self.signal_name)
        self._image_width_config.set(self.signal_name, "image_width", str(None))
        self._image_width_config.write(open(self.config_file, 'w'))
        self._image_line_repeat_config = ConfigParser.ConfigParser()
        self._image_line_repeat_config.read(self.config_file)
        if not self._image_line_repeat_config.has_section(self.signal_name):
        	self._image_line_repeat_config.add_section(self.signal_name)
        self._image_line_repeat_config.set(self.signal_name, "image_line_repeat", str(None))
        self._image_line_repeat_config.write(open(self.config_file, 'w'))
        self._image_file_name_config = ConfigParser.ConfigParser()
        self._image_file_name_config.read(self.config_file)
        if not self._image_file_name_config.has_section(self.signal_name):
        	self._image_file_name_config.add_section(self.signal_name)
        self._image_file_name_config.set(self.signal_name, "image_file_name", str(None))
        self._image_file_name_config.write(open(self.config_file, 'w'))

    def get_config_file(self):
        return self.config_file

    def set_config_file(self, config_file):
        self.config_file = config_file
        self._tx_frequency_config = ConfigParser.ConfigParser()
        self._tx_frequency_config.read(self.config_file)
        if not self._tx_frequency_config.has_section(self.signal_name):
        	self._tx_frequency_config.add_section(self.signal_name)
        self._tx_frequency_config.set(self.signal_name, "tx_frequency", str(None))
        self._tx_frequency_config.write(open(self.config_file, 'w'))
        self._tune_offset_config = ConfigParser.ConfigParser()
        self._tune_offset_config.read(self.config_file)
        if not self._tune_offset_config.has_section(self.signal_name):
        	self._tune_offset_config.add_section(self.signal_name)
        self._tune_offset_config.set(self.signal_name, "tune_offset", str(None))
        self._tune_offset_config.write(open(self.config_file, 'w'))
        self._samp_rate_config = ConfigParser.ConfigParser()
        self._samp_rate_config.read(self.config_file)
        if not self._samp_rate_config.has_section(self.signal_name):
        	self._samp_rate_config.add_section(self.signal_name)
        self._samp_rate_config.set(self.signal_name, "samp_rate", str(None))
        self._samp_rate_config.write(open(self.config_file, 'w'))
        self._ota_config = ConfigParser.ConfigParser()
        self._ota_config.read(self.config_file)
        if not self._ota_config.has_section(self.signal_name):
        	self._ota_config.add_section(self.signal_name)
        self._ota_config.set(self.signal_name, "ota", str(None))
        self._ota_config.write(open(self.config_file, 'w'))
        self._message_text_config = ConfigParser.ConfigParser()
        self._message_text_config.read(self.config_file)
        if not self._message_text_config.has_section(self.signal_name):
        	self._message_text_config.add_section(self.signal_name)
        self._message_text_config.set(self.signal_name, "message_text", str(None))
        self._message_text_config.write(open(self.config_file, 'w'))
        self._message_font_config = ConfigParser.ConfigParser()
        self._message_font_config.read(self.config_file)
        if not self._message_font_config.has_section(self.signal_name):
        	self._message_font_config.add_section(self.signal_name)
        self._message_font_config.set(self.signal_name, "message_font", str(None))
        self._message_font_config.write(open(self.config_file, 'w'))
        self._image_width_config = ConfigParser.ConfigParser()
        self._image_width_config.read(self.config_file)
        if not self._image_width_config.has_section(self.signal_name):
        	self._image_width_config.add_section(self.signal_name)
        self._image_width_config.set(self.signal_name, "image_width", str(None))
        self._image_width_config.write(open(self.config_file, 'w'))
        self._image_line_repeat_config = ConfigParser.ConfigParser()
        self._image_line_repeat_config.read(self.config_file)
        if not self._image_line_repeat_config.has_section(self.signal_name):
        	self._image_line_repeat_config.add_section(self.signal_name)
        self._image_line_repeat_config.set(self.signal_name, "image_line_repeat", str(None))
        self._image_line_repeat_config.write(open(self.config_file, 'w'))
        self._image_file_name_config = ConfigParser.ConfigParser()
        self._image_file_name_config.read(self.config_file)
        if not self._image_file_name_config.has_section(self.signal_name):
        	self._image_file_name_config.add_section(self.signal_name)
        self._image_file_name_config.set(self.signal_name, "image_file_name", str(None))
        self._image_file_name_config.write(open(self.config_file, 'w'))
        self._device_string_config = ConfigParser.ConfigParser()
        self._device_string_config.read(self.config_file)
        if not self._device_string_config.has_section('main'):
        	self._device_string_config.add_section('main')
        self._device_string_config.set('main', "device_string", str(None))
        self._device_string_config.write(open(self.config_file, 'w'))
        self.offset_tx_0.set_config_file(self.config_file)

    def get_tx_frequency(self):
        return self.tx_frequency

    def set_tx_frequency(self, tx_frequency):
        self.tx_frequency = tx_frequency
        self.offset_tx_0.set_tx_frequency(self.tx_frequency)

    def get_tune_offset(self):
        return self.tune_offset

    def set_tune_offset(self, tune_offset):
        self.tune_offset = tune_offset
        self.offset_tx_0.set_tune_offset(self.tune_offset)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.offset_tx_0.set_samp_rate(self.samp_rate)

    def get_ota(self):
        return self.ota

    def set_ota(self, ota):
        self.ota = ota
        self.offset_tx_0.set_ota(self.ota)

    def get_message_text(self):
        return self.message_text

    def set_message_text(self, message_text):
        self.message_text = message_text
        self.epy_txt_to_image.message_text = self.message_text

    def get_message_font(self):
        return self.message_font

    def set_message_font(self, message_font):
        self.message_font = message_font
        self.epy_txt_to_image.message_font = self.message_font

    def get_image_width(self):
        return self.image_width

    def set_image_width(self, image_width):
        self.image_width = image_width
        self.epy_txt_to_image.image_width = self.image_width

    def get_image_line_repeat(self):
        return self.image_line_repeat

    def set_image_line_repeat(self, image_line_repeat):
        self.image_line_repeat = image_line_repeat

    def get_image_file_name(self):
        return self.image_file_name

    def set_image_file_name(self, image_file_name):
        self.image_file_name = image_file_name
        self.epy_txt_to_image.image_file_name = self.image_file_name

    def get_device_string(self):
        return self.device_string

    def set_device_string(self, device_string):
        self.device_string = device_string
        self.offset_tx_0.set_device_string(self.device_string)


def main(top_block_cls=signal, options=None):

    tb = top_block_cls()
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
