#!/usr/bin/env python

from pyitpp import itload
from matplotlib.pyplot import *

out = itload('pccc_bersim_awgn.it')

semilogy(out['EbN0_dB'], out['BER'].T, 'o-')
grid()
xlabel('$E_b/N_0$')
ylabel('$BER$')
title('PCCC performance in AWGN channel')
show()
