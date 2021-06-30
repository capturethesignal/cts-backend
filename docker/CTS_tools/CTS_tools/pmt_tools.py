#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# Capture the Signal
# Author: Jonathan Andersson
##################################################

#import os
#script_path = os.path.dirname(os.path.realpath(__file__))
#os.chdir(script_path)

#import sys
#sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

import pmt

def pmt_dict(d):

    p = pmt.make_dict()

    for k, v in d.iteritems():
        p = pmt.dict_add(p, pmt.intern(k), pmt.to_pmt(v))

    print p
    return p

def main():
    #print pmt_dict({"x":0})
    #print pmt.cons(pmt_dict({"x":0}), pmt.intern("d"))
    #sync_bytes = "AA" #[0x00, 0x00]
    #print pmt_dict({"sync_word": sync_bytes, })
    #print pmt.cons(pmt_dict({"sync_word": sync_bytes, }), pmt.to_pmt(sync_bytes))
    return

if __name__ == '__main__':
    main()
