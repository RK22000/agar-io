import tensorflow as tf
from tensorflow import keras
from keras import layers
import os
import matplotlib.pyplot as plt
from math import ceil
import numpy as np

input_shape = (1400, 2240, 3)

# Gray scaling and resizing
h = 50
w = h*input_shape[1]//input_shape[0]
preproc_layers = [
    layers.Rescaling(1./255, name='scaling_0-1'),
    # tf.image.rgb_to_grayscale,
    layers.Resizing(h, w, name=f'sizing_{h}-{w}')
    # layers.Resizing(50,50)
]
def preproc(x):
    for step in preproc_layers:
        x = step(x)
    return x
preproc_shape = (50, 80, 3)

inputs = keras.Input(shape=input_shape, name="Screen Input Layer")
preprocess = preproc(inputs)
intermediate = [
    layers.Conv2D(32, 5, input_shape=preprocess.shape),
    layers.MaxPool2D(),
    layers.Conv2D(10, 5),
    layers.MaxPool2D(),
    layers.Flatten(),
    layers.Dense(1000, activation='relu'),
    layers.Dense(100, activation='relu'),
]
# process = keras.Input(shape=preprocess.shape, name="Input Preprocessed Layer")
process = preprocess
for i, layer in enumerate(intermediate):
    process = layer(process)
    intermediate[i] = process
out_X = layers.Dense(10, activation=keras.activations.softmax)(process)
out_Y = layers.Dense(10, activation=keras.activations.softmax)(process)

coord_X = tf.argmax(out_X, 1)/10*input_shape[0]
coord_Y = tf.argmax(out_Y, 1)/10*input_shape[1]


class CoordCrossEntropyLoss(keras.losses.Loss):
    def __call__(self, y_true, y_pred, sample_weight=None):
        y_true = tf.reshape(y_true,(-1,))
        # print(y_true)
        trimmed = [min(i.numpy(),0.9) for i in y_true]
        # print(trimmed)
        y_true = [tf.one_hot(round(i*10), 10) for i in trimmed]
        y_true = tf.stack(y_true, 0)
        # print(y_true)
        y_pred = tf.reshape(y_pred, (-1, 10))
        return keras.losses.binary_crossentropy(y_true, y_pred)


model = keras.Model(preprocess, layers.concatenate([out_X, out_Y]))
model_X = keras.Model(inputs, coord_X)
model_Y = keras.Model(inputs, coord_Y)