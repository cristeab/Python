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
if 0 == out['type']:
    filt_type = 'low'
elif 1 == out['type']:
    filt_type = 'high'
else:
    filt_type = ''
[B, A] = butter(out['order'], float(out['fc'])/(out['fs']/2.0), btype=filt_type)
filt_signal = lfilter(B, A, in_sig, axis=0)
ref_fft_sig = fft.fft(filt_signal, N)

figure(0)
plot(freq[0:N/2], abs(fft_sig)[0:N/2], 'b', label='C - abs')
plot(freq[0:N/2], angle(fft_sig)[N/2:N]/(2*pi), 'g', label='C - angle')

plot(freq[0:N/2], abs(ref_fft_sig)[0:N/2], 'b--', label='P - abs')
plot(freq[0:N/2], angle(ref_fft_sig)[N/2:N]/(2*pi), 'g--', label='P - angle')
grid()
legend()
show()
