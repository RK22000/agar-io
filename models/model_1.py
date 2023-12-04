'''
Model takes an input image of dimensions (200,213)
This input dimention is produced by doing focus image 
'''
import tensorflow as tf
from tensorflow import keras
from keras import layers
import numpy as np
import utils
import os
import time

model = keras.Sequential(layers=[
    layers.Conv2D(32, (5,5), input_shape=(200,213,3), activation='relu'),
    layers.MaxPool2D((5,5)),
    layers.Conv2D(32, (5,5), activation='relu'),
    layers.MaxPool2D((5,5)),
    layers.Flatten(),
    layers.Dense(1000, 'relu'),
    layers.Dense(1000, 'relu'),
    layers.Dense(100, 'relu'),
    layers.Dense(2, 'softmax'),
])
# model.save_weights("blank.h5")
# model.summary()
if os.path.exists("some.h5"):
    print("loading weights")
    model.load_weights("some.h5")
    # converter = tf.lite.TFLiteConverter.from_keras_model(model)
    # converter.optimizations = [tf.lite.Optimize.DEFAULT]
    # model = converter.convert()

angles = [i*45 for i in range(8)]
radians = [i*np.pi/180 for i in angles]
vecs = [np.array((np.cos(i), np.sin(i))) for i in radians]

def tstart():
    global t
    t = time.time()
def tstop(s):
    global t
    print(f"{s}: {time.time()-t}")
    tstart()

def predict(img, screen_shape=(2240,1400)):
    tstart()
    screen_shape = np.array(screen_shape)
    tstop("got shape")
    # imgs = [utils.focus_dir(img, i) for i in angles]
    imgs = utils.focus_dirs(img, angles)
    tstop("got focus dirs")
    # imgs = [np.asarray(i) for i in imgs]
    imgs = np.asarray(imgs)/255
    tstop("converted to np.arrays")
    # imgs = tf.constant(imgs)/255
    # tstop("divided by 255")
    preds = model(imgs)
    tstop("made predations")
    print(f"Model Preds: \n{preds}")
    direction = tf.argmax(preds)[1].numpy()
    print(f"Pred max: {direction}: {preds[direction]}")
    prev = direction-1 if direction > 0 else 7
    nxt = direction+1 if direction < 7 else 0
    next_dirs = [prev,direction,nxt]
    # angles = [dirs[i]*np.pi/180 for i in next_dirs]
    mags = [preds[i][1] for i in next_dirs]
    dirs = [vecs[i] for i in next_dirs]
    go = sum([a*b for a,b in zip(mags, dirs)])/3

    direction = tf.argmax(preds)[0].numpy()
    print(f"Pred min: {preds[direction]}")
    prev = direction-1 if direction > 0 else 7
    nxt = direction+1 if direction < 7 else 0
    next_dirs = [prev,direction,nxt]
    # angles = [dirs[i]*np.pi/180 for i in next_dirs]
    mags = [preds[i][0] for i in next_dirs]
    dirs = [vecs[i] for i in next_dirs]
    avoid = sum([a*b for a,b in zip(mags, dirs)])/3

    pos = (-avoid)/2
    # def angle_to_vec(a, mag):
    #     vec = np.array((np.cos(a),np.sin(a)))*0.25*screen_shape
    #     vec += screen_shape/2
    #     return vec*mag
    # vecs = [angle_to_vec(i,j) for i,j in zip(angles,mags)]

    # x = sum([i for i,j in vecs])/3
    # y = sum([j for i,j in vecs])/3
    # pos = np.array([x,y])
    
    # mags = [preds[i][1] for i in move]
    # angle = dirs[direction]*np.pi/180
    # pos = np.array((np.cos(angle),np.sin(angle)))
    pos *= 0.25*screen_shape
    pos += screen_shape/2
    # pos *= preds[direction][1]
    return pos

    
    

