import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

def build_model():
    inputs = keras.Input(shape=(10 * 15))

    dense = layers.Dense(8, activation="relu")
    x = dense(inputs)

    x = layers.Dense(8, activation="relu")(x)
    outputs = layers.Dense(17, activation="softmax")(x)

    model = keras.Model(inputs=inputs, outputs=outputs, name="g729_dtmf_model")
    return model

model = build_model()
model.summary()

from read_g729_data import read_g729_norm
from os import listdir

from os.path import isfile, join
import numpy as np

X = []
Y = []

PIDXS = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'H', 'M')

onlyfiles = lambda mypath: [f for f in listdir(mypath) if isfile(join(mypath, f))]
pdir = 'training_data/positive'
ndir = 'training_data/negative'
pfiles = onlyfiles(pdir)
nfiles = onlyfiles(ndir)
for pfile in pfiles:
    d = read_g729_norm(join(pdir, pfile))
    #print(d, len(d))
    #sys.exit(0)
    parr = [0,] * 17
    dsym = pfile.split('_', 2)[1]
    parr[PIDXS.index(dsym)] = 1
    X.append(d.flatten())
    Y.append(np.array(parr))

nres = np.array((0,)*16 + (1,))
for nfile in nfiles:
    d = read_g729_norm(join(ndir, nfile))
    X.append(d.flatten())
    Y.append(nres)
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
train_dataset = train_dataset.shuffle(buffer_size=10 * 1024).batch(15)

# Prepare the validation dataset
#val_dataset = tf.data.Dataset.from_tensor_slices((x_val, y_val))
#val_dataset = val_dataset.batch(64)

model.fit(train_dataset, epochs=1000)
#model.fit(x, y, epochs=100, batch_size=15)
test_scores = model.evaluate(x, y, verbose=2)

print("Test loss:", test_scores[0])
print("Test accuracy:", test_scores[1])

predictions = model.predict(x[:20])

print("predictions:", predictions)
print("results:", y[:20])
