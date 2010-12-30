# File:   pyitpp.py
# Brief:  Loads an IT++ itfile content and outputs a dictionary with all found variables
# Author: Bogdan Cristea
#
# Usage: from pyitpp import itload
#        out = itload('fname.it')
#
# This module provides a function for loading itfile content into matrices/scalars
# and outputs all these variables as a dictionary whose keys are variable names.
# All required functions/classes from python modules (numpy, sys, os, stat, struct)
# are loaded, be aware about possible name clashes (e.g. mat) 
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
        elif 'dvec' == var_type:
            length = unpack('L', f.read(8))[0]
            fmt = str(length)+'d'
            out[var_name] = mat(unpack(fmt, f.read(length*8)), 'float64').T#convert to a column vector
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