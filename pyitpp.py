# File:   pyitpp.py
# Brief:  Loads an IT++ itfile content and outputs a dictionary with all found variables.
# Author: Bogdan Cristea
#
# Usage: from pyitpp import itload
#        out = itload('fname.it')
#
# This module provides a function for loading itfile content into matrices/scalars
# and outputs all these variables as a dictionary whose keys are variable names as
# found in itfile. This module uses numpy module for matrix operations.
# Thus the provided functionality is similar to itload() function from MATLAB.
#
# -------------------------------------------------------------------------
#
# Copyright (C) 1995-2010  (see AUTHORS file for a list of contributors)
#
# This file is part of IT++ - a C++ library of mathematical, signal
# processing, speech processing, and communications classes and functions.
#
# IT++ is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# IT++ is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along
# with IT++.  If not, see <http://www.gnu.org/licenses/>.
#
# -------------------------------------------------------------------------

from sys import exit
from os import stat
from os import SEEK_SET
from stat import ST_SIZE
from struct import unpack
from numpy import mat
from numpy import reshape
from numpy import zeros

def __fgetstr(fid):
    str = ''
    while 1:
        d = fid.read(1);
        if d == '\x00':
            break
        str = str+d;
    return str

def itload(in_file):
    
    try:
        f = open(in_file, 'rb')
    except IOError:
        try:
            f = open(in_file+'.it', 'rb')
        except IOError:            
            print 'Cannot open file'
            exit()
    
    #get file size
    file_size = stat(in_file)[ST_SIZE]
    
    #read IT++ magic string
    magic = f.read(4);
    if 'IT++' != magic:
        print 'Not an IT++ file!'
        exit()
    
    #check the IT++ file version
    version = f.read(1)
    if 3 != ord(version):
        print 'Only IT++ file version 3 is supported by this function!'
        exit()
    
    out = dict()#use a dictionary to output all tuples read from it file
    
    while 1:
        #save current file position
        pos = f.tell()
        
        #read header, data, and total block sizes (3*uint64)
        header_data_block_sizes = unpack('LLL', f.read(24))
        
        #read current variable name
        var_name = __fgetstr(f)
        #read current variable type
        var_type = __fgetstr(f)
        #skip header bytes
        f.seek(pos+header_data_block_sizes[0], SEEK_SET)
        
        if len(var_type) == 0: #A deleted entry -> skip it
            pass
        #scalars
        # --- bin ---
        elif 'bin' == var_type:
            out[var_name] = unpack('b', f.read(1))[0]
        # --- int8 (char) ---
        elif 'int8' == var_type:
            out[var_name] = unpack('c', f.read(1))[0]
        # --- int16 (short) ---
        elif 'int16' == var_type:
            out[var_name] = unpack('h', f.read(2))[0]
        # --- int32 (int) ---
        elif 'int32' == var_type:
            out[var_name] = unpack('i', f.read(4))[0]
        # --- float32 (float) ---
        elif 'float32' == var_type:
            out[var_name] = unpack('f', f.read(4))[0]
        # --- float64 (double) ---
        elif 'float64' == var_type:
            out[var_name] = unpack('d', f.read(8))[0]
        # --- cfloat32 (complex<float>) ---
        elif 'cfloat32' == var_type:
            real_imag = unpack('2f', f.read(8))
            out[var_name] = complex(real_imag[0], real_imag[1])
        # --- cfloat64 (complex<double>) ---
        elif 'cfloat64' == var_type:
            real_imag = unpack('2d', f.read(16))
            out[var_name] = complex(real_imag[0], real_imag[1])
        
        #vectors
        # --- bvec ---
        elif 'bvec' == var_type:
            length = unpack('L', f.read(8))[0]
            fmt = str(length)+'b'
            out[var_name] = mat(unpack(fmt, f.read(length)), 'uint8').T#convert to a column vector
        # --- string ---
        elif 'string' == var_type:
            length = unpack('L', f.read(8))[0]
            fmt = str(length)+'c'
            out[var_name] = "".join(unpack(fmt, f.read(length)))
        # --- svec ---
        elif 'svec' == var_type:
            length = unpack('L', f.read(8))[0]
            fmt = str(length)+'h'
            out[var_name] = mat(unpack(fmt, f.read(length*2)), 'int16').T#convert to a column vector
        # --- ivec ---
        elif 'ivec' == var_type:
            length = unpack('L', f.read(8))[0]
            fmt = str(length)+'i'
            out[var_name] = mat(unpack(fmt, f.read(length*4)), 'int32').T#convert to a column vector
        # --- fvec ---
        elif 'fvec' == var_type:
            length = unpack('L', f.read(8))[0]
            fmt = str(length)+'f'
            out[var_name] = mat(unpack(fmt, f.read(length*4)), 'float32').T#convert to a column vector
        # --- dvec ---
        elif 'dvec' == var_type:
            length = unpack('L', f.read(8))[0]
            fmt = str(length)+'d'
            out[var_name] = mat(unpack(fmt, f.read(length*8)), 'float64').T#convert to a column vector
        # --- fcvec ---
        elif 'fcvec' == var_type:
            length = unpack('L', f.read(8))[0]
            fmt = str(2*length)+'f'
            real_imag = mat(unpack(fmt, f.read(2*length*4)), 'float32').T#convert to a column vector
            out[var_name] = zeros((length, 1));
            for i in range(length):
                out[var_name][i,0] = complex(real_imag[2*i], real_imag[2*i+1])
        # --- dcvec ---
        elif 'dcvec' == var_type:
            length = unpack('L', f.read(8))[0]
            fmt = str(2*length)+'d'
            real_imag = mat(unpack(fmt, f.read(2*length*8)), 'float64').T#convert to a column vector
            out[var_name] = zeros((length, 1), complex);
            for i in range(length):
                out[var_name][i,0] = complex(real_imag[2*i], real_imag[2*i+1])        
        
        #matrices
        elif 'dmat' == var_type:
            rows = unpack('L', f.read(8))[0]
            cols = unpack('L', f.read(8))[0]
            fmt = str(rows*cols)+'d'
            out[var_name] = reshape(mat(unpack(fmt, f.read(rows*cols*8)), 'float64'), (cols, rows)).T
        else:
            print 'Not a supported type: ', var_type
    
        if pos+header_data_block_sizes[2] >= file_size:
            break
        else:
            f.seek(pos+header_data_block_sizes[2], SEEK_SET)
    
    f.close()
    return out