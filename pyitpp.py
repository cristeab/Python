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