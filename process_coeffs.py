#process coefficients

from pyitpp import itload
from pylab import *

out = itload('coeffs.it')

figure(0)
for i in range(0, 8):
    freq_idx = 'freq_range['+str(i)+']'
    Alow_idx = 'pAlow['+str(i)+',:]'
    plot(out[Alow_idx], 'o-')
    Blow_idx = 'pBlow['+str(i)+',:]'
    plot(out[Blow_idx], 'o-')    
grid()
title('Lowpass')

figure(1)
for i in range(0, 8):
    Ahigh_idx = 'pAhigh['+str(i)+',:]'
    plot(out[Ahigh_idx], 'o-')
    Bhigh_idx = 'pBhigh['+str(i)+',:]'
    plot(out[Bhigh_idx], 'o-')    
grid()
title('Highpass')

figure(2)
for i in range(0, 7):
    Apass_idx = 'pApass['+str(i)+',:]'
    plot(out[Apass_idx], 'o-')
    Bpass_idx = 'pBpass['+str(i)+',:]'
    plot(out[Bpass_idx], 'o-')
grid()
title('Bandpass')

figure(3)
for i in range(0, 7):
    Astop_idx = 'pAstop['+str(i)+',:]'
    plot(out[Astop_idx], 'o-')
    Bstop_idx = 'pBstop['+str(i)+',:]'
    plot(out[Bstop_idx], 'o-')
grid()
title('Stopband')

show()
