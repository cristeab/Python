#!/usr/bin/env python

from pyitpp import itload
import unittest
from numpy import mat
from numpy.matlib import zeros

class TestITLoad(unittest.TestCase):

    def setUp(self):
        self.out = itload('../C++/IT++_trial/test_pyitpp.it')
        self.eps = 1e-6

    def test_scalars(self):
        # test all supported scalars for type and value
        self.assertEqual(type(self.out['a']).__name__, 'uint8')
        self.assertEqual(self.out['a'], 1)
        
        self.assertEqual(type(self.out['b']).__name__, 'str')
        self.assertEqual(self.out['b'], '2')
        
        self.assertEqual(type(self.out['c']).__name__, 'int16')
        self.assertEqual(self.out['c'], -3)
        
        self.assertEqual(type(self.out['d']).__name__, 'int32')
        self.assertEqual(self.out['d'], -4)
        
        self.assertEqual(type(self.out['e']).__name__, 'float32')
        self.assertTrue(abs(self.out['e']-5.67) < self.eps)
        
        self.assertEqual(type(self.out['f']).__name__, 'float64')
        self.assertTrue(abs(self.out['f']-8.91234567) < self.eps)
        
        self.assertEqual(type(self.out['g']).__name__, 'complex64')
        self.assertTrue(abs(self.out['g']-complex(-1.234, 4.321)) < self.eps)
        
        self.assertEqual(type(self.out['h']).__name__, 'complex128')
        self.assertTrue(abs(self.out['h']-complex(-1.234567, 4.321654)) < self.eps)

    def test_vectors(self):
        # test all supported vectors for type and value
        self.assertEqual(type(self.out['i']).__name__, 'matrix')
        self.assertEqual(type(self.out['i'][0,0]).__name__, 'uint8')
        self.assertTrue((self.out['i'] == mat('0; 1; 1; 0; 0; 1')).all())
        
        self.assertEqual(type(self.out['j']).__name__, 'str')
        self.assertEqual(self.out['j'], 'abc')
        
        self.assertEqual(type(self.out['k']).__name__, 'matrix')
        self.assertEqual(type(self.out['k'][0,0]).__name__, 'int16')
        self.assertTrue((self.out['k'] == mat('10; 11; 12; 13; 14; 15; 16; 17; 18; 19')).all())
        
        self.assertEqual(type(self.out['l']).__name__, 'matrix')
        self.assertEqual(type(self.out['l'][0,0]).__name__, 'int32')
        self.assertTrue((self.out['l'] == mat('20; 21; 22; 23; 24; 25; 26; 27; 28; 29')).all())
        
        self.assertEqual(type(self.out['m']).__name__, 'matrix')
        self.assertEqual(type(self.out['m'][0,0]).__name__, 'float64')
        self.assertTrue((abs(self.out['m']-mat('30; 31; 32; 33; 34; 35; 36; 37; 38; 39')) < self.eps).all())
        
        self.assertEqual(type(self.out['n']).__name__, 'matrix')
        self.assertEqual(type(self.out['n'][0,0]).__name__, 'complex128')
        step = complex(0.5, -0.5)
        ref_cvec = zeros((10, 1), complex)
        ref_cvec[0,0] = complex(0.0, 0.0)
        for i in range(1, 10):
            ref_cvec[i,0] = ref_cvec[i-1,0]+step
        self.assertTrue((abs(self.out['n']-ref_cvec) < self.eps).all())
        
    def test_matrices(self):
        # test all supported matrices for type and value
        self.assertEqual(type(self.out['o']).__name__, 'matrix')
        self.assertEqual(type(self.out['o'][0,0]).__name__, 'uint8')
        self.assertTrue((self.out['o'] == mat('0, 1, 1; 0, 0, 1')).all())

        self.assertEqual(type(self.out['p']).__name__, 'matrix')
        self.assertEqual(type(self.out['p'][0,0]).__name__, 'int16')
        self.assertTrue((self.out['p'] == mat('1, 2, 3; 4, 5, 6')).all())

        self.assertEqual(type(self.out['q']).__name__, 'matrix')
        self.assertEqual(type(self.out['q'][0,0]).__name__, 'int32')
        self.assertTrue((self.out['q'] == mat('11, 12, 13; 14, 15, 16')).all())

        self.assertEqual(type(self.out['r']).__name__, 'matrix')
        self.assertEqual(type(self.out['r'][0,0]).__name__, 'float64')
        self.assertTrue((abs(self.out['r']-mat('1.5, 1.6, 1.7; 2.3, 2.4, 2.5')) < self.eps).all())

        self.assertEqual(type(self.out['s']).__name__, 'matrix')
        self.assertEqual(type(self.out['s'][0,0]).__name__, 'complex128')
        step = complex(0.5, -0.5)
        ref_cvec = zeros((3, 2), complex)
        ref_cvec[0,0] = complex(0.0, 0.0)
        for i in range(1,3):
            ref_cvec[i,0] = ref_cvec[i-1,0]+step
        ref_cvec[0,1] = complex(1.5, -1.5)
        for i in range(1,3):
            ref_cvec[i,1] = ref_cvec[i-1,1]+step
        self.assertTrue((abs(self.out['s']-ref_cvec) < self.eps).all())
    
    def test_arrays_of_scalars(self):
        self.assertEqual(type(self.out['t']).__name__, 'list')
        self.assertEqual(type(self.out['t'][0]).__name__, 'uint8')
        self.assertTrue(self.out['t'] == [0, 1, 0, 1, 1, 0, 0, 0, 1])
        
        self.assertEqual(type(self.out['u']).__name__, 'list')
        self.assertEqual(type(self.out['u'][0]).__name__, 'int16')
        self.assertTrue(self.out['u'] == [0, 1, 2, 3, 4, 5, 6, 7, 8])
        
        self.assertEqual(type(self.out['v']).__name__, 'list')
        self.assertEqual(type(self.out['v'][0]).__name__, 'int32')
        self.assertTrue(self.out['v'] == [10, 11, 12, 13, 14, 15, 16, 17, 18])
        
        self.assertEqual(type(self.out['w']).__name__, 'list')
        self.assertEqual(type(self.out['w'][0]).__name__, 'float32')
        ref_farray = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8]
        for i in range(len(self.out['w'])):
            self.assertTrue(abs(self.out['w'][i]-ref_farray[i]) < self.eps)
        
        self.assertEqual(type(self.out['x']).__name__, 'list')
        self.assertEqual(type(self.out['x'][0]).__name__, 'float64')
        ref_farray = [1.2222, 2.3333, 3.44444, 4.55555]
        for i in range(len(self.out['x'])):
            self.assertTrue(abs(self.out['x'][i]-ref_farray[i]) < self.eps)
            
        self.assertEqual(type(self.out['y']).__name__, 'list')
        self.assertEqual(type(self.out['y'][0]).__name__, 'complex64')
        ref_cfarray = list()
        ref_cfarray.append(complex(0.0, 0.0))
        step = complex(0.5, -0.5)
        for i in range(1, 10):
            ref_cfarray.append(ref_cfarray[i-1]+step)
        for i in range(len(self.out['y'])):
            self.assertTrue(abs(self.out['y'][i]-ref_cfarray[i]) < self.eps)
        
        self.assertEqual(type(self.out['z']).__name__, 'list')
        self.assertEqual(type(self.out['z'][0]).__name__, 'complex128')
        ref_cfarray = list()
        ref_cfarray.append(complex(0.0, 0.0))
        step = complex(-0.5, 0.5)
        for i in range(1, 10):
            ref_cfarray.append(ref_cfarray[i-1]+step)
        for i in range(len(self.out['z'])):
            self.assertTrue(abs(self.out['z'][i]-ref_cfarray[i]) < self.eps)
            
    def test_arrays_of_vectors(self):
        self.assertEqual(type(self.out['aa']).__name__, 'list')
        self.assertEqual(type(self.out['aa'][0]).__name__, 'matrix')
        self.assertEqual(type(self.out['aa'][0][0,0]).__name__, 'uint8')
        ref_bvarray = [mat((1, 1, 1, 0, 0, 0, 1)).T, mat((0, 0, 1, 1)).T, mat((1, 0, 1)).T]
        for i in range(3):
            self.assertTrue((self.out['aa'][i] == ref_bvarray[i]).all())
        
        self.assertEqual(type(self.out['bb']).__name__, 'list')
        self.assertEqual(type(self.out['bb'][0]).__name__, 'matrix')
        self.assertEqual(type(self.out['bb'][0][0,0]).__name__, 'int16')
        ref_svarray = [mat((1, 1, 1, 2, 3, 0, 1)).T, mat((0, 6, 1, 1)).T, mat((1, 7, 1)).T]
        for i in range(3):
            self.assertTrue((self.out['bb'][i] == ref_svarray[i]).all())

        self.assertEqual(type(self.out['cc']).__name__, 'list')
        self.assertEqual(type(self.out['cc'][0]).__name__, 'matrix')
        self.assertEqual(type(self.out['cc'][0][0,0]).__name__, 'int32')
        ref_ivarray = [mat((10, 10, 10, 20, 30, 0, 10)).T, mat((0, 60, 10, 10)).T, mat((10, 70, 10)).T]
        for i in range(3):
            self.assertTrue((self.out['cc'][i] == ref_ivarray[i]).all())

        self.assertEqual(type(self.out['dd']).__name__, 'list')
        self.assertEqual(type(self.out['dd'][0]).__name__, 'matrix')
        self.assertEqual(type(self.out['dd'][0][0,0]).__name__, 'float64')
        ref_dvarray = [mat((0.1, 0.1, 0.1, 0.2, 0.3, 0.0, 0.1)).T, mat((0.0, 0.6, 0.1, 0.1)).T, mat((0.1, 0.7, 0.1)).T]
        for i in range(3):
            self.assertTrue((abs(self.out['dd'][i]-ref_dvarray[i]) < self.eps).all())
            
        self.assertEqual(type(self.out['ee']).__name__, 'list')
        self.assertEqual(type(self.out['ee'][0]).__name__, 'matrix')
        self.assertEqual(type(self.out['ee'][0][0,0]).__name__, 'complex128')
        step = complex(0.5, -0.5)
        tmp = zeros((5, 1), complex)
        tmp[0,0] = complex(0.0, 0.0)
        for i in range(1, 5):
            tmp[i,0] = tmp[i-1,0]+step
        ref_cvarray = list()
        ref_cvarray.append(tmp)
        ref_cvarray.append(tmp[0:3])
        ref_cvarray.append(tmp[1:5])
        for i in range(3):
            self.assertTrue((abs(self.out['ee'][i]-ref_cvarray[i]) < self.eps).all())
            
        self.assertEqual(type(self.out['gg']).__name__, 'list')
        self.assertEqual(type(self.out['gg'][0]).__name__, 'str')
        ref_cvarray = ['abcd', 'abc', 'defghijk']
        for i in range(3):
            self.assertEqual(self.out['gg'][i], ref_cvarray[i])        
    
    def test_arrays_of_matrices(self):
        self.assertEqual(type(self.out['hh']).__name__, 'list')
        self.assertEqual(type(self.out['hh'][0]).__name__, 'matrix')
        self.assertEqual(type(self.out['hh'][0][0,0]).__name__, 'uint8')
        ref_bmarray = [mat('1, 1; 1, 0; 0, 1'), mat('0, 0, 1; 1, 0, 1'), mat('1; 0; 1')]
        for i in range(3):
            self.assertTrue((self.out['hh'][i] == ref_bmarray[i]).all())
            
        self.assertEqual(type(self.out['ii']).__name__, 'list')
        self.assertEqual(type(self.out['ii'][0]).__name__, 'matrix')
        self.assertEqual(type(self.out['ii'][0][0,0]).__name__, 'int16')
        ref_smarray = [mat('1, 2; 1, 3; 4, 7'), mat('4, 7, 1; 8, 6, 1'), mat('3; 8; 5')]
        for i in range(3):
            self.assertTrue((self.out['ii'][i] == ref_smarray[i]).all())

        self.assertEqual(type(self.out['jj']).__name__, 'list')
        self.assertEqual(type(self.out['jj'][0]).__name__, 'matrix')
        self.assertEqual(type(self.out['jj'][0][0,0]).__name__, 'int32')
        ref_imarray = [mat('11, 21; 11, 31; 41, 71'), mat('41, 71, 11; 81, 61, 11'), mat('31; 81; 51')]
        for i in range(3):
            self.assertTrue((self.out['jj'][i] == ref_imarray[i]).all())

        self.assertEqual(type(self.out['kk']).__name__, 'list')
        self.assertEqual(type(self.out['kk'][0]).__name__, 'matrix')
        self.assertEqual(type(self.out['kk'][0][0,0]).__name__, 'float64')
        ref_dmarray = [mat('1.1, 2.1; 1.1, 3.1; 4.1, 7.1'), mat('4.1, 7.1, 1.1; 8.1, 6.1, 1.1'), mat('3.1; 8.1; 5.1')]
        for i in range(3):
            self.assertTrue((self.out['kk'][i] == ref_dmarray[i]).all())
            
        self.assertEqual(type(self.out['ll']).__name__, 'list')
        self.assertEqual(type(self.out['ll'][0]).__name__, 'matrix')
        self.assertEqual(type(self.out['ll'][0][0,0]).__name__, 'complex128')
        step = complex(0.5, -0.5)
        tmp = zeros((3, 2), complex)
        tmp[0,0] = complex(0.0, 0.0)
        for i in range(1,3):
            tmp[i,0] = tmp[i-1,0]+step
        tmp[0,1] = complex(1.5, -1.5)
        for i in range(1,3):
            tmp[i,1] = tmp[i-1,1]+step
        ref_cmarray = list()
        ref_cmarray.append(tmp)
        ref_cmarray.append(tmp[0:2][0:2])
        ref_cmarray.append(tmp[0:1][0:2])
        for i in range(3):
            self.assertTrue((self.out['ll'][i] == ref_cmarray[i]).all())        

if __name__ == '__main__':
    unittest.main()
