import pyautogui as pygui
from PIL.Image import Image
from PIL import ImageDraw
import numpy as np
from math import sqrt
import os
import tensorflow as tf

model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=pygui.size()),
    tf.keras.layers.Dense(2)
])

print(model.summary())

model.compile(
    optimizer='sgd',
    loss=tf.keras.losses.MeanSquaredError(),
    jit_compile=True
)

# def fit_pics():
    


pic_count = 0
def get_shot():
    pos = np.array(pygui.position())
    name = os.path.join("pics", str(pic_count)+"_"+"x".join(pos.astype(str))+".png")
    pic_count += 1
    img: Image = pygui.screenshot(name)
    draw = ImageDraw.Draw(img)
    rdiag = 10*sqrt(2)
    draw.ellipse([tuple(pos-rdiag),tuple(pos+rdiag)], fill="red")
    img.save(name)

get_shot()

