import utils
t = utils.loading_text("Loading Tensorflow")
t.start()
import tensorflow as tf
from tensorflow import keras
from keras import layers
t.stop()
import os
import numpy as np
import time

model = tf.keras.Sequential(layers=[
    tf.keras.layers.Conv2D(10, 5, input_shape=(200,320,3), activation='relu'),
    tf.keras.layers.MaxPool2D(5),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(100, 'relu'),
    tf.keras.layers.Dense(6, 'sigmoid'),
])

model.load_weights("try_again.keras")

def load_student(stu_file):
    # model.load_weights(stu_file)
    print(f"Loaded Model {stu_file}")


react_time=0
react_count=0.000001
def reset_reaction_time():
    global react_time, react_count
    react_time=0
    react_count=0.000001


dir_count = 6
angles = [i*360/dir_count for i in range(6)]
radians = [i*np.pi/180 for i in angles]
vecs = [np.array((np.cos(i), np.sin(i))) for i in radians]

def predict(img):
    rt = time.time()
    res = _predict(img)
    rt = time.time()-rt
    global react_time, react_count
    react_time += rt
    react_count += 1
    return res

frac = 0
def _predict(img):
    img = np.asarray(img, np.float32)/255
    img = np.stack([img])
    preds = model(img)[0]
    mags = preds
    dirs = vecs
    pos = -sum([a*b for a,b in zip(mags, dirs)])


    # direction = tf.argmax(preds).numpy()
    # direction = (direction+dir_count//2)%dir_count
    # # print(f"Pred max: {direction}: {preds[direction]}")
    # prev = direction-1 if direction > 0 else dir_count-1
    # nxt = direction+1 if direction < dir_count-1 else 0
    # next_dirs = [prev,direction,nxt]
    # mags = [1-preds[i] for i in next_dirs]
    # dirs = [vecs[i] for i in next_dirs]
    # go = sum([a*b for a,b in zip(mags, dirs)])/3

    # direction = tf.argmax(preds).numpy()
    # # print(f"Pred min: {direction}: {preds[direction]}")
    # prev = direction-1 if direction > 0 else dir_count-1
    # nxt = direction+1 if direction < dir_count-1 else 0
    # next_dirs = [prev,direction,nxt]
    # mags = [preds[i] for i in next_dirs]
    # # mags = np.exp(mags)/sum(np.exp(mags))
    # dirs = [vecs[i] for i in next_dirs]
    # avoid = sum([a*b for a,b in zip(mags, dirs)])

    # # frac=0
    # pos = (frac*go-(1-frac)*avoid)
    pos *= 0.25
    pos += 0.5
    return pos
