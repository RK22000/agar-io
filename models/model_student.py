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

model = keras.Sequential(layers=[
    layers.Conv2D(32, (5,5), input_shape=(200,320,3), activation='relu'),
    layers.MaxPool2D((5,5)),
    layers.Conv2D(32, (5,5), activation='relu'),
    layers.MaxPool2D((5,5)),
    layers.Flatten(),
    layers.Dense(1000, 'relu'),
    layers.Dense(1000, 'relu'),
    layers.Dense(100, 'relu'),
    layers.Dense(6, 'sigmoid'),
])

if os.path.exists("student5.keras"):
    print("loading weights")
    model.load_weights("student5.keras")

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

def _predict(img):
    img = np.asarray(img, np.float32)/255
    img = np.stack([img])
    preds = model(img)[0]

    direction = tf.argmax(preds).numpy()
    direction = (direction+dir_count//2)%dir_count
    # print(f"Pred max: {direction}: {preds[direction]}")
    prev = direction-1 if direction > 0 else dir_count-1
    nxt = direction+1 if direction < dir_count-1 else 0
    next_dirs = [prev,direction,nxt]
    mags = [1-preds[i] for i in next_dirs]
    dirs = [vecs[i] for i in next_dirs]
    go = sum([a*b for a,b in zip(mags, dirs)])/3

    direction = tf.argmax(preds).numpy()
    # print(f"Pred min: {direction}: {preds[direction]}")
    prev = direction-1 if direction > 0 else dir_count-1
    nxt = direction+1 if direction < dir_count-1 else 0
    next_dirs = [prev,direction,nxt]
    mags = [preds[i] for i in next_dirs]
    # mags = np.exp(mags)/sum(np.exp(mags))
    dirs = [vecs[i] for i in next_dirs]
    avoid = sum([a*b for a,b in zip(mags, dirs)])

    frac=0
    pos = (frac*go-(1-frac)*avoid)
    pos *= 0.25
    pos += 0.5
    return pos
