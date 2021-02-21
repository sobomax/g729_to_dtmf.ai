import sys

NC0_B = 7
NC1_B = 5
BIT_1 = 0x0081
bitsno = (1+NC0_B, # MA + 1st stage
          NC1_B*2, #2nd stage
          8,1,  13,4, 7, # first subframe
          5,    13,4, 7) # second subframe

def bin2int(no_of_bits, frame):
    value = 0
    for i in range(0, no_of_bits):
        value <<= 1
        bit = frame & 0xffff
        frame >>= 16
        if bit == BIT_1:
            value += 1
    return(value);

def parametersBitStream2Array(bitStream):
    parameters = []
    parameters.append((bitStream[0] >> 7) & 0x1)
    parameters.append(bitStream[0] & 0x7f)
    parameters.append((bitStream[1] >> 3) & 0x1f);
    parameters.append(((bitStream[1] & 0x7) << 2) | ((bitStream[2] >> 6) & 0x3))
    parameters.append((bitStream[2] & 0x3f) << 2 | ((bitStream[3] >> 6) & 0x3))
    parameters.append((bitStream[3] >> 5) & 0x1)
    parameters.append((((bitStream[3] & 0x1f)) << 8) | bitStream[4])
    parameters.append((bitStream[5] >> 4) & 0xf)
    parameters.append((bitStream[5] >> 1) & 0x7)
    parameters.append(((bitStream[5] & 0x1) << 3) | ((bitStream[6] >> 5) & 0x7))
    parameters.append(bitStream[6] & 0x1f)
    parameters.append(((bitStream[7]) << 5) | ((bitStream[8] >> 3) & 0x1f))
    parameters.append(((bitStream[8] & 0x7) << 1) | ((bitStream[9] >> 7) & 0x1))
    parameters.append((bitStream[9] >> 4) & 0x7)
    parameters.append(bitStream[9] & 0xf)
    return parameters

def read_g729(fname):
    cfile = open(fname, 'rb')
    res = []
    while True:
        b10 = cfile.read(10)
        if len(b10) == 0:
            break
        bytes = [x for x in b10]
        res.append(parametersBitStream2Array(bytes))
    return res
#        bytes.reverse()
#        frame = 0
#        for b1 in bytes:
#            frame <<= 8
#            frame |= b1
#        bstr = bin(frame)[2:]
#        s_bstr = '%s%s' % ('0' * (80 - len(bstr)), bstr)
#        coeffs = []
#        for bsize in bitsno:
#            msk = (2**bsize) - 1
#            coeffs.append(frame & msk)
#            frame >>= bsize
#            #coeffs.append(bin2int(bsize, frame))
#
#        print(s_bstr, len(s_bstr))
#        #print(coeffs)

data = read_g729('dtmf_2021_H_02_H_18.18')
#print(data)

import numpy as np
ndata = np.transpose(np.array(data))

import matplotlib.pyplot as plt
#plt.imshow(a, cmap='rainbow', interpolation='nearest', extent=[0,len(data),0,len(data[0])], aspect=10000)
#plt.savefig('dtmf_2021_H_02_H_18.png')

def forceAspect(ax,aspect):
    im = ax.get_images()
    extent =  im[0].get_extent()
    ax.set_aspect(abs((extent[1]-extent[0])/(extent[3]-extent[2]))/aspect)

fig = plt.figure()
ax = fig.add_subplot(111)

sum_of_rows = ndata.sum(axis=1)
normalized_array = ndata / sum_of_rows[:, np.newaxis]

ax.imshow(normalized_array, cmap='rainbow', interpolation='nearest')
forceAspect(ax, aspect=4)
fig.savefig('dtmf_2021_H_02_H_18.png', bbox_inches='tight', dpi=300)
