import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

from g729_nn_model import build_g729_model, g729_model_ovec

model = build_g729_model(compile = False)
model.summary()
keras.utils.plot_model(model, "multi_input_and_output_model.png", show_shapes=True)

from read_g729_data import read_g729_norm
from os import listdir

from os.path import isfile, join
import numpy as np

import scipy.fft #.fft.dct((1,3,4,5))

def read_g729_flat(fname):
    d = read_g729_norm(fname)
    #res = []
    #for row in np.transpose(d):
    #    res.append(scipy.fft.dct(row))
    #d = np.array(res)
    #sys.exit(1)
    return d.flatten()

X = []
Y = []
X_val = []
Y_val = []

onlyfiles = lambda mypath: [f for f in listdir(mypath) if isfile(join(mypath, f))]
pdir = 'training_data/positive'
ndir = 'training_data/negative'
vdir = 'training_data/validate'
pfiles = onlyfiles(pdir)
nfiles = onlyfiles(ndir)
vfiles = onlyfiles(vdir)
for pfile in pfiles:
    d = read_g729_flat(join(pdir, pfile))
    #print(d, len(d))
    #sys.exit(0)
    parr = [0,] * 17
    dsym = pfile.split('_', 2)[1]
    parr[g729_model_ovec.index(dsym)] = 1
    X.append(d)
    Y.append(np.array(parr))

nres = np.array((0,)*16 + (1,))
for nfile in nfiles:
    d = read_g729_flat(join(ndir, nfile))
    X.append(d)
    Y.append(nres)

for vfile in vfiles:
    d = read_g729_flat(join(vdir, vfile))
    X_val.append(d)
    if vfile.startswith('dtmf_'):
        parr = [0,] * 17
        dsym = vfile.split('_', 2)[1]
        parr[g729_model_ovec.index(dsym)] = 1
        narr = np.array(parr)
        Y_val.append(narr)
        #X.append(d)
        #Y.append(narr)
    else:
        Y_val.append(nres)

#print(d)
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
#model.compile(
#    optimizer=keras.optimizers.RMSprop(),  # Optimizer
#    # Loss function to minimize
#    loss='binary_crossentropy',
#    # List of metrics to monitor
#    metrics=['accuracy'],
#)

print(len(X), len(Y))

x = np.array(X)
y = np.array(Y)

train_dataset = tf.data.Dataset.from_tensor_slices((X, Y))
train_dataset = train_dataset.shuffle(buffer_size=10 * 1024).batch(20)

# Prepare the validation dataset

x_val = np.array(X_val)
y_val = np.array(Y_val)

val_dataset = tf.data.Dataset.from_tensor_slices((x_val, y_val))
val_dataset = val_dataset.batch(64)

model.fit(train_dataset, epochs=100, validation_data=val_dataset)
#model.fit(x, y, epochs=100, batch_size=15)
test_scores = model.evaluate(x, y, verbose=2)

print("Test loss:", test_scores[0])
print("Test accuracy:", test_scores[1])

predictions = model.predict(x[:20])

print("predictions:", predictions)
print("results:", y[:20])

test_stream = read_g729_norm('dtmf_2021_H_02_H_18.vol1.0.18')
i = 0
while i < len(test_stream):
    tf = test_stream[i:i + 10]
    if len(tf) < 10:
        break

    #res = []
    #for row in np.transpose(tf):
    #    res.append(scipy.fft.dct(row))
    #tf = np.array(res).flatten()
    tf = tf.flatten()

    predictions = model.predict(np.array([tf,]))
    didx = np.argmax(predictions)
    dtmf = g729_model_ovec[didx]
    if dtmf != None:
        print(i, dtmf, predictions[0][didx])
        i += 10
    else:
        i += 1
        if i % 10 == 0:
            print('_')
