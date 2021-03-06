from pyitpp import itload
from pylab import *
from numpy import *
from math import pi
from scipy.signal import butter, lfilter

out = itload('in_out_signals.it')
sig_len = len(out['out_sig'])
in_sig = array(out['in_sig'])[:,0].tolist()
sig = array(out['out_sig'])[:,0].tolist()

time = range(0, sig_len)

N = 1024
fft_sig = fft.fft(sig, N)
freq = []
for i in range(0, N):
    freq.append((i*2*pi/N)/(2*pi))

#reference filter
order = int(out['order'])
if 0 == int(out['type']):
    filt_type = 'lowpass'
    Wn = float(out['fc'])/(float(out['fs'])/2.0)
elif 1 == int(out['type']):
    filt_type = 'highpass'
    Wn = float(out['fc'])/(float(out['fs'])/2.0)
elif 2 == int(out['type']):
    filt_type = 'bandpass'
    Wn = [float(out['fl'])/(float(out['fs'])/2.0), float(out['fh'])/(float(out['fs'])/2.0)]
elif 3 == int(out['type']):
    filt_type = 'bandstop'
    Wn = [float(out['fl'])/(float(out['fs'])/2.0), float(out['fh'])/(float(out['fs'])/2.0)]
else:
    print 'unknown filter type'
    filt_type = 'none'

#generate filter
[B, A] = butter(order, Wn, btype=filt_type)
filt_signal = lfilter(B, A, in_sig, axis=0)
ref_fft_sig = fft.fft(filt_signal, N)

print 'order =', order
print 'Wn =', Wn
print ' ', 'A', 'B'
for i in range(0, len(A)):
    print i, A[i], B[i]

figure(0)
plot(freq[0:N/2], abs(fft_sig)[0:N/2], 'b', label='C - abs')
plot(freq[0:N/2], angle(fft_sig)[N/2:N]/(2*pi), 'g', label='C - angle')

plot(freq[0:N/2], abs(ref_fft_sig)[0:N/2], 'b--', label='P - abs')
plot(freq[0:N/2], angle(ref_fft_sig)[N/2:N]/(2*pi), 'g--', label='P - angle')
grid()
legend()
title('Amplitude and phase of the FFT of the output signal')

figure(1)
plot(in_sig, label='input')
plot(sig, 'r', label='output')
grid()
legend()
title('Input and output signal')

show()
