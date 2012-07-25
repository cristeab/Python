#compare the output of the filters in fixed point with
#the reference implementation (double)

from pyitpp import itload
from pylab import *
from scipy.signal import butter, lfilter
from numpy import *
from math import pi

out = itload('testFilt.it')

norm_freq = float(out['norm_freq'])
norm_freq_h = float(out['norm_freq_h'])
length = int(out['length'])
in_sig = array(out['pSignal'])[:,0].tolist()
N = 1024
order = 2

#generate time and frequency supports
time = range(0, length)
freq = []
for i in range(0, N):
    freq.append((i*2*pi/N)/(2*pi))

# lowpass

#generate filter
[B, A] = butter(order, 2*norm_freq, btype='lowpass')

#get filtered signal
filt_sig = array(out['fx_pOutSignal_low'])[:,0].tolist()

#get reference filtered signal
ref_filt_sig = lfilter(B, A, in_sig, axis=0)

#FFT
fft_sig = fft.fft(filt_sig, N)
ref_fft_sig = fft.fft(ref_filt_sig, N)

figure(0)
plot(freq[0:N/2], abs(fft_sig)[0:N/2], 'b', label='amp')
plot(freq[0:N/2], angle(fft_sig)[N/2:N]/(2*pi), 'g', label='angle')
plot(freq[0:N/2], abs(ref_fft_sig)[0:N/2], 'b--', label='ref - amp')
plot(freq[0:N/2], angle(ref_fft_sig)[N/2:N]/(2*pi), 'g--', label='ref - angle')
legend()
grid()
title('Lowpass')

#compare output with reference
def get_error(ref_filt_sig, filt_sig):
    err = []
    for i in time:
        err.append(ref_filt_sig[i]-filt_sig[i])
    return err

figure(4)
plot(get_error(ref_filt_sig, filt_sig), label='Lowpass')

# highpass

#generate filter
[B, A] = butter(order, 2*norm_freq, btype='highpass')

#get filtered signal
filt_sig = array(out['fx_pOutSignal_high'])[:,0].tolist()

#get reference filtered signal
ref_filt_sig = lfilter(B, A, in_sig, axis=0)

#FFT
fft_sig = fft.fft(filt_sig, N)
ref_fft_sig = fft.fft(ref_filt_sig, N)

figure(1)
plot(freq[0:N/2], abs(fft_sig)[0:N/2], 'b', label='amp')
plot(freq[0:N/2], angle(fft_sig)[N/2:N]/(2*pi), 'g', label='angle')
plot(freq[0:N/2], abs(ref_fft_sig)[0:N/2], 'b--', label='ref - amp')
plot(freq[0:N/2], angle(ref_fft_sig)[N/2:N]/(2*pi), 'g--', label='ref - angle')
legend()
grid()
title('Highpass')

figure(4)
plot(get_error(ref_filt_sig, filt_sig), label='highpass')

# bandpass

#generate filter
[B, A] = butter(order, [2*norm_freq, 2*norm_freq_h], btype='bandpass')

#get filtered signal
filt_sig = array(out['fx_pOutSignal_pass'])[:,0].tolist()

#get reference filtered signal
ref_filt_sig = lfilter(B, A, in_sig, axis=0)

#FFT
fft_sig = fft.fft(filt_sig, N)
ref_fft_sig = fft.fft(ref_filt_sig, N)

figure(2)
plot(freq[0:N/2], abs(fft_sig)[0:N/2], 'b', label='amp')
plot(freq[0:N/2], angle(fft_sig)[N/2:N]/(2*pi), 'g', label='angle')
plot(freq[0:N/2], abs(ref_fft_sig)[0:N/2], 'b--', label='ref - amp')
plot(freq[0:N/2], angle(ref_fft_sig)[N/2:N]/(2*pi), 'g--', label='ref - angle')
legend()
grid()
title('Bandpass')

figure(4)
plot(get_error(ref_filt_sig, filt_sig), label='bandpass')

# bandstop

#generate filter
[B, A] = butter(order, [2*norm_freq, 2*norm_freq_h], btype='bandstop')

#get filtered signal
filt_sig = array(out['fx_pOutSignal_stop'])[:,0].tolist()

#get reference filtered signal
ref_filt_sig = lfilter(B, A, in_sig, axis=0)

#FFT
fft_sig = fft.fft(filt_sig, N)
ref_fft_sig = fft.fft(ref_filt_sig, N)

figure(3)
plot(freq[0:N/2], abs(fft_sig)[0:N/2], 'b', label='ref - amp')
plot(freq[0:N/2], angle(fft_sig)[N/2:N]/(2*pi), 'g', label='ref - angle')
plot(freq[0:N/2], abs(ref_fft_sig)[0:N/2], 'b--', label='ref - amp')
plot(freq[0:N/2], angle(ref_fft_sig)[N/2:N]/(2*pi), 'g--', label='ref - angle')
legend()
grid()
title('Bandstop')

figure(4)
plot(get_error(ref_filt_sig, filt_sig), label='bandstop')
legend()
grid()
title('Output error')

show()
