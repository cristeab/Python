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
        self.assertEqual(type(self.out['a']).__name__, 'int')
        self.assertEqual(self.out['a'], 1)
        
        self.assertEqual(type(self.out['b']).__name__, 'str')
        self.assertEqual(self.out['b'], '2')
        
        self.assertEqual(type(self.out['c']).__name__, 'int')
        self.assertEqual(self.out['c'], -3)
        
        self.assertEqual(type(self.out['d']).__name__, 'int')
        self.assertEqual(self.out['d'], -4)
        
        self.assertEqual(type(self.out['e']).__name__, 'float')
        self.assertTrue(abs(self.out['e']-5.67) < self.eps)
        
        self.assertEqual(type(self.out['f']).__name__, 'float')
        self.assertTrue(abs(self.out['f']-8.91234567) < self.eps)
        
        self.assertEqual(type(self.out['g']).__name__, 'complex')
        self.assertTrue(abs(self.out['g']-complex(-1.234, 4.321)) < self.eps)
        
        self.assertEqual(type(self.out['h']).__name__, 'complex')
        self.assertTrue(abs(self.out['h']-complex(-1.234567, 4.321654)) < self.eps)

    def test_vectors(self):
        # test all supported vectors for type and value
        self.assertEqual(type(self.out['i']).__name__, 'matrix')
        self.assertTrue((self.out['i'] == mat('0; 1; 1; 0; 0; 1')).all())
        
        self.assertEqual(type(self.out['j']).__name__, 'str')
        self.assertEqual(self.out['j'], 'abc')
        
        self.assertEqual(type(self.out['k']).__name__, 'matrix')
        self.assertTrue((self.out['k'] == mat('10; 11; 12; 13; 14; 15; 16; 17; 18; 19')).all())
        
        self.assertEqual(type(self.out['l']).__name__, 'matrix')
        self.assertTrue((self.out['l'] == mat('20; 21; 22; 23; 24; 25; 26; 27; 28; 29')).all())
        
        self.assertEqual(type(self.out['m']).__name__, 'matrix')
        self.assertTrue((abs(self.out['m']-mat('30; 31; 32; 33; 34; 35; 36; 37; 38; 39')) < self.eps).all())
        
        self.assertEqual(type(self.out['n']).__name__, 'matrix')
        step = complex(0.5, -0.5)
        ref_cvec = zeros((10, 1), complex)
        ref_cvec[0,0] = complex(0.0, 0.0)
        for i in range(1, 10):
            ref_cvec[i,0] = ref_cvec[i-1,0]+step
        self.assertTrue((abs(self.out['n']-ref_cvec) < self.eps).all())
        
    def test_matrices(self):
        # test all supported matrices for type and value
        self.assertEqual(type(self.out['o']).__name__, 'matrix')
        self.assertTrue((self.out['o'] == mat('0, 1, 1; 0, 0, 1')).all())

        self.assertEqual(type(self.out['p']).__name__, 'matrix')
        self.assertTrue((self.out['p'] == mat('1, 2, 3; 4, 5, 6')).all())

        self.assertEqual(type(self.out['q']).__name__, 'matrix')
        self.assertTrue((self.out['q'] == mat('11, 12, 13; 14, 15, 16')).all())

        self.assertEqual(type(self.out['r']).__name__, 'matrix')
        self.assertTrue((abs(self.out['r']-mat('1.5, 1.6, 1.7; 2.3, 2.4, 2.5')) < self.eps).all())

        self.assertEqual(type(self.out['s']).__name__, 'matrix')
        step = complex(0.5, -0.5)
        ref_cvec = zeros((3, 2), complex)
        ref_cvec[0,0] = complex(0.0, 0.0)
        for i in range(1,3):
            ref_cvec[i,0] = ref_cvec[i-1,0]+step
        ref_cvec[0,1] = complex(1.5, -1.5)
        for i in range(1,3):
            ref_cvec[i,1] = ref_cvec[i-1,1]+step
        self.assertTrue((abs(self.out['s']-ref_cvec) < self.eps).all())  

if __name__ == '__main__':
    unittest.main()
