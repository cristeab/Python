#!/usr/bin/env python

import pyitpp as itpp

in_file = '/home/bogdan/C++/IT++_trial/pccc_bersim_awgn.it'
out = itpp.itload(in_file)
print out.keys()
for key in out.keys():
    print out[key].shape
