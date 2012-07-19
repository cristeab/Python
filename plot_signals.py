from pyitpp import itload
from pylab import *
from numpy import *
from math import pi

out = itload('in_out_signals.it')
sig_len = len(out['out_sig'])
sig = array(out['out_sig'])[:,0].tolist()

time = range(0, sig_len)

fft_sig = fft.fft(sig, 1024)
N = len(fft_sig)
freq = []
for i in range(0, N):
    freq.append(i*2*pi/N)

figure(0)
plot(freq[0:N/2], abs(fft_sig)[0:N/2])
plot(freq[0:N/2], angle(fft_sig)[N/2:N]/(2*pi))
grid()
show()
