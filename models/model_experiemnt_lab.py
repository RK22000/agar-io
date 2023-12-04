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

tflite_path = "model.tflite"
interpreter = tf.lite.Interpreter(model_path=tflite_path)
lite_model = interpreter.get_signature_runner('serving_default')

# angles = [i*45 for i in range(8)]
angles = [i*90 for i in range(4)]
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
    imgs = np.asarray(imgs, np.float32)/255
    tstop("converted to np.arrays")
    # imgs = tf.constant(imgs)/255
    # tstop("divided by 255")
    preds = lite_model(conv2d_input=imgs)['dense_3']
    tstop("made predations")
    print(f"Model Preds: \n{preds}")
    direction = tf.argmax(preds)[1].numpy()
    print(f"Pred max: {direction}: {preds[direction]}")
    prev = direction-1 if direction > 0 else 3
    nxt = direction+1 if direction < 3 else 0
    next_dirs = [prev,direction,nxt]
    # angles = [dirs[i]*np.pi/180 for i in next_dirs]
    mags = [preds[i][1] for i in next_dirs]
    dirs = [vecs[i] for i in next_dirs]
    go = sum([a*b for a,b in zip(mags, dirs)])/3

    direction = tf.argmax(preds)[0].numpy()
    print(f"Pred min: {preds[direction]}")
    prev = direction-1 if direction > 0 else 3
    nxt = direction+1 if direction < 3 else 0
    next_dirs = [prev,direction,nxt]
    # angles = [dirs[i]*np.pi/180 for i in next_dirs]
    mags = [preds[i][0] for i in next_dirs]
    dirs = [vecs[i] for i in next_dirs]
    avoid = sum([a*b for a,b in zip(mags, dirs)])

    pos = (-avoid)
    pos *= 0.25*screen_shape
    pos += screen_shape/2
    return pos

    
    

