#!/usr/bin/env python

import matplotlib.pyplot as plt
from scipy.signal import lfilter, butter
from scipy import *
from math import pi
from math import sin

Wn = 0.2
order = 2
filt_type = 'pass'
length = 100
omega = pi/6.0
N = 1024

time = range(0, length)
signal = []
for i in time:
    signal.append(0.0)
#    signal.append(sin(omega*i))
signal[0] = 1

if 'low' == filt_type or 'high' == filt_type:
    [B, A] = butter(order, Wn, btype=filt_type)
elif 'pass' == filt_type:
    [B, A] = butter(order, [Wn, 0.5-Wn], btype=filt_type)
out_signal = lfilter(B, A, signal)

fft_signal = fft(out_signal, N)
freq = []
for i in range(0, N):
    freq.append(i*1.0/N)

plt.plot(freq[0:N/2], abs(fft_signal[0:N/2]))
#plt.plot(freq[0:N/2], angle(fft_signal[0:N/2]))
plt.grid()
plt.show()
