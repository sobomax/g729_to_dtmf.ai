from tensorflow import keras
from tensorflow.keras import layers

g729_model_ovec = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'H', 'M', None)

def build_g729_model(compile = True):
    inputs = keras.Input(shape=(10 * 15))
    dense = layers.Dense(32, activation="relu")
    x = dense(inputs)
    x = layers.Dense(24, activation="relu")(x)
    outputs = layers.Dense(17, activation="softmax")(x)

    model = keras.Model(inputs=inputs, outputs=outputs, name="g729_dtmf_model")

    if compile:
        model.compile(loss='categorical_crossentropy', optimizer='rmsprop', \
          metrics=['categorical_accuracy'])
    return model

