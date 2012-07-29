#!/usr/bin/env python
#computes data gain factor for biquad filters

from scipy.signal import lfilter
from decimal import *

TWOPLACES = Decimal(10) ** -2       # same as Decimal('0.01')
def mul(x, y, fp=TWOPLACES):
    return (x * y).quantize(fp)
def div(x, y, fp=TWOPLACES):
    return (x / y).quantize(fp)
def fix(x, fp=TWOPLACES):
    return Decimal(x).quantize(fp)

Q_factor = 15
coeff_scaling = 2.0

QPLACES = Decimal('10')**-Q_factor

B = [0.63895378694532, 1.27498563369662, 0.63895378694532]
A = [1.0, 1.14511388070077, 0.437307900103239]

#scale coeffs
A_scale = []
B_scale = []
for i in range(0, len(B)):
    A_scale.append(A[i]/coeff_scaling)
    B_scale.append(B[i]/coeff_scaling)

#feedback transfer function

N = 1000
#kronecker_imp = [1.0]
#for i in range(0, N-1):
#    kronecker_imp.append(0.0)

#filt_sig = lfilter([1], A_scale, kronecker_imp, axis=0)

#G = abs(filt_sig[0])
#for i in range(1, N):
#    G = G+abs(filt_sig[i])

#print G

def get_scale_factor(A):
    d = [1.0/A[0], -A[1]/(A[0]*A[0]), 0.0]
    eps = 1e-6
    G = abs(d[0])+abs(d[1])
    for i in range(0, N):
        d[2] = -(A[1]/A[0])*d[1]-(A[2]/A[0])*d[0]
        diff = abs(d[2])
        if diff < eps:
            break
        G = G + diff
        d[0] = d[1]
        d[1] = d[2]
    return G, i

#second method
[G, i] = get_scale_factor(A_scale)
print G, "at", i

#convert to hex
for i in range(0, len(A_scale)):
    print fix(A_scale[i], QPLACES), fix(B_scale[i], QPLACES)

print int(fix(A_scale[0])/QPLACES)
