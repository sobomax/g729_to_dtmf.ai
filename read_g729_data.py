import sys
import numpy as np
import matplotlib.pyplot as plt

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

def forceAspect(ax,aspect):
    im = ax.get_images()
    extent =  im[0].get_extent()
    ax.set_aspect(abs((extent[1]-extent[0])/(extent[3]-extent[2]))/aspect)

if __name__ == '__main__':
    ifname = sys.argv[1]
    ofname = ifname.rsplit('.', 1)[0] + '.png'
    data = read_g729(ifname)
    nframes = len(data)

    b10 = [x for x in b'\xff' * 10]
    maxvals = np.array(parametersBitStream2Array(b10))
    ndata = np.array(data)
    #print(maxvals)
    normalized_array = ndata / maxvals
    #print(normalized_array)

    ndata = np.transpose(normalized_array)

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.imshow(ndata, cmap='gray', interpolation='nearest')
    forceAspect(ax, aspect=(4 * nframes / 600))
    fig.savefig(ofname, bbox_inches='tight', dpi=300)
    print('%s generated' % (ofname,))
