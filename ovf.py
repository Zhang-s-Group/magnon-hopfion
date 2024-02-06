#!/usr/bin/python

import numpy as np
import struct

# readOvf(path)
# writeOvf(path, config, data)
def readOvf(path):
    data = np.empty(1)
    config = {}
    xnodes = 1
    ynodes = 1
    znodes = 1
    valuedim = 3

    f = open(path, "rb")

    data_block_begin_flag = 0
    while True:
        line = f.readline()
        line = line.lower()
        rbound = line.find(b'##')
        if rbound != -1:
            line = line[0:rbound]
        line = line.strip()

        if data_block_begin_flag == 1:
            if line.find(b'end: data') == -1:
                print(line)
                raise Exception(b'Unexpected size of data block.');
            data_block_begin_flag = 2
            break
            
        if line.find(b'xbase') != -1:
            config['xbase'] = float(line[9:])
        if line.find(b'ybase') != -1:
            config['ybase'] = float(line[9:])
        if line.find(b'zbase') != -1:
            config['zbase'] = float(line[9:])
        if line.find(b'xstepsize') != -1:
            config['xstepsize'] = float(line[13:])
        if line.find(b'ystepsize') != -1:
            config['ystepsize'] = float(line[13:])
        if line.find(b'zstepsize') != -1:
            config['zstepsize'] = float(line[13:])
        if line.find(b'xnodes') != -1:
            config['xnodes'] = xnodes = int(line[10:])
        if line.find(b'ynodes') != -1:
            config['ynodes'] = ynodes = int(line[10:])
        if line.find(b'znodes') != -1:
            config['znodes'] = znodes = int(line[10:])
        if line.find(b'xmax') != -1:
            config['xmax'] = float(line[8:])
        if line.find(b'ymax') != -1:
            config['ymax'] = float(line[8:])
        if line.find(b'zmax') != -1:
            config['zmax'] = float(line[8:])
        if line.find(b'xmin') != -1:
            config['xmin'] = float(line[8:])
        if line.find(b'ymin') != -1:
            config['ymin'] = float(line[8:])
        if line.find(b'zmin') != -1:
            config['zmin'] = float(line[8:])
        if line.find(b'valuemultiplier') != -1:
            config['valuemultiplier'] = float(line[19:])
        if line.find(b'valuedim') != -1:
            config['valuedim'] = valuedim = int(line[12:])

        if line.find(b'begin: data') != -1:
            datatype = line[14:]
            for key in ['znodes', 'ynodes', 'xnodes', 'valuedim']:
                assert key in config
            # ordered with x incremented first, then y, and finally z.
            data = readDataBlock(f, datatype, xnodes*ynodes*znodes*valuedim).reshape(znodes, ynodes, xnodes, valuedim)
            data_block_begin_flag = 1
        if line.find(b'end: data') != -1:
            if data_block_begin_flag == 0:
                raise Exception("Data block ends without \"begin\".")

    f.close()

    if 'valuemultiplier' in config:
        data *= valuemultiplier
        config['valuemultiplier'] = 1
    if data_block_begin_flag != 2:
        raise Exception("Data block does not exist.")
    
    for necessary_key in ['xnodes', 'ynodes', 'znodes', 'xstepsize', 'ystepsize', 'zstepsize']:
        assert necessary_key in config
    if not 'xmin' in config:
        config['xmin'] = 0.
    if not 'ymin' in config:
        config['ymin'] = 0.
    if not 'zmin' in config:
        config['zmin'] = 0.
    if not 'xmax' in config:
        config['xmax'] = config['xmin'] + config['xnodes'] * config['xstepsize']
    if not 'ymax' in config:
        config['ymax'] = config['ymin'] + config['ynodes'] * config['ystepsize']
    if not 'zmax' in config:
        config['zmax'] = config['zmin'] + config['znodes'] * config['zstepsize']
    if not 'xbase' in config:
        config['xbase'] = 0.5 * config['xstepsize']
    if not 'ybase' in config:
        config['ybase'] = 0.5 * config['ystepsize']
    if not 'zbase' in config:
        config['zbase'] = 0.5 * config['zstepsize']
    return {'config': config, 'data': data}



def readDataBlock(f, datatype, count):
    data = np.empty(1)

    if datatype == b'binary 4':
        magic = f.read(4)
        if magic == b'\x38\xb4\x96\x49':
            data = np.fromfile(f, dtype='<f', count=count)
        elif magic == b'\x49\x96\xb4\x38':
            data = np.fromfile(f, dtype='>f', count=count)
        else:
            raise Exception("Data block does not begin with 1234567.0.");
        data = np.fromfile(f, dtype='<f', count=count)
    elif datatype == b'binary 8':
        magic = f.read(8)
        if magic != b'\x40\xde\x77\x83\x21\x12\xdc\x42':
            data = np.fromfile(f, dtype='<d', count=count)
        elif magic != b'\x42\xdc\x12\x21\x83\x77\xde\x40':
            data = np.fromfile(f, dtype='>d', count=count)
        else:
            raise Exception("Data block does not begin with 123456789012345.0.");
    elif datatype == b'text':
        raise Exception("Text representation of data block is not support.")
    else:
        raise Exception("Datatype \""+datatype+"\" is not supported.")

    return data


def writeOvf(path, config, data):
    f = open(path, 'wb')
    f.write(b'# OOMMF OVF 2.0\n')
    f.write(b'# Segment count: 1\n')
    f.write(b'# Begin: Segment\n')
    writeHeader(f, config)
    writeData(f, data)
    f.write(b'# End: Segment\n')
    f.close()

def writeHeader(f, config):
    for necessary_key in ['xnodes', 'ynodes', 'znodes', 'xstepsize', 'ystepsize', 'zstepsize']:
        assert necessary_key in config
    if not 'xmin' in config:
        config['xmin'] = 0.
    if not 'ymin' in config:
        config['ymin'] = 0.
    if not 'zmin' in config:
        config['zmin'] = 0.
    if not 'xmax' in config:
        config['xmax'] = config['xmin'] + config['xnodes'] * config['xstepsize']
    if not 'ymax' in config:
        config['ymax'] = config['ymin'] + config['ynodes'] * config['ystepsize']
    if not 'zmax' in config:
        config['zmax'] = config['zmin'] + config['znodes'] * config['zstepsize']
    if not 'xbase' in config:
        config['xbase'] = 0.5 * config['xstepsize']
    if not 'ybase' in config:
        config['ybase'] = 0.5 * config['ystepsize']
    if not 'zbase' in config:
        config['zbase'] = 0.5 * config['zstepsize']
    f.write(\
b""" # Begin: Header
# Title: m
# meshtype: rectangular
# meshunit: m
# xmin: %e
# ymin: %e
# zmin: %e
# xmax: %e
# ymax: %e
# zmax: %e
# valuedim: 3
# valuelabels: m_x m_y m_z
# valueunits: 1 1 1
# Desc: Total simulation time:  0  s
# xbase: %e
# ybase: %e
# zbase: %e
# xnodes: %d
# ynodes: %d
# znodes: %d
# xstepsize: %e
# ystepsize: %e
# zstepsize: %e
# End: Header
""" \
        % (config['xmin'], config['ymin'], config['zmin'], 
        config['xmax'], config['ymax'], config['zmax'], 
        config['xbase'], config['ybase'], config['zbase'], 
        config['xnodes'], config['ynodes'], config['znodes'], 
        config['xstepsize'], config['ystepsize'], config['zstepsize']))

def writeData(f, data, dtype='<d'):
    data = data.flatten()
    if dtype == '<d':
        f.write(b'# Begin: Data Binary 8\n')
        f.write(b'\x40\xde\x77\x83\x21\x12\xdc\x42')
        bindata = struct.pack('<%dd' % data.size, *data)
        f.write(bindata)
        f.write(b'# End: Data Binary 8\n')
    elif dtype == '>d':
        f.write(b'# Begin: Data Binary 8\n')
        f.write(b'\x42\xdc\x12\x21\x83\x77\xde\x40')
        bindata = struct.pack('>%dd' % data.size, *data)
        f.write(bindata)
        f.write(b'# End: Data Binary 8\n')
    elif dtype == '<f':
        f.write(b'# Begin: Data Binary 4\n')
        f.write(b'\x38\xb4\x96\x49')
        bindata = struct.pack('<%df' % data.size, *data)
        f.write(bindata)
        f.write(b'# End: Data Binary 4\n')
    elif dtype == '>f':
        f.write(b'# Begin: Data Binary 4\n')
        f.write(b'\x49\x96\xb4\x38')
        bindata = struct.pack('>%df' % data.size, *data)
        f.write(bindata)
        f.write(b'# End: Data Binary 4\n')
    else:
        raise Exception("Unknown dtype for writing data. ")
