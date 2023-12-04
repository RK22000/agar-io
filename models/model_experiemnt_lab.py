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

dir_count = 6
angles = [i*360/dir_count for i in range(6)]
radians = [i*np.pi/180 for i in angles]
vecs = [np.array((np.cos(i), np.sin(i))) for i in radians]

def tstart():
    # global t
    # t = time.time()
    pass
def tstop(s):
    # global t
    # print(f"{s}: {time.time()-t}")
    # tstart()
    pass
frac=0.5
react_time=0
react_count=0.000001
def reset_reaction_time():
    global react_time, react_count
    react_time=0
    react_count=0.000001

def predict(img, screen_shape=(2240,1400)):
    rt = time.time()
    res = _predict(img, screen_shape)
    rt = time.time()-rt
    global react_time, react_count
    react_time += rt
    react_count += 1
    return res

def _predict(img, screen_shape=(2240,1400)):
    tstart()
    screen_shape = np.array(screen_shape)
    tstop("got shape")
    imgs = utils.focus_dirs(img, angles)
    tstop("got focus dirs")
    imgs = np.asarray(imgs, np.float32)/255
    tstop("converted to np.arrays")
    preds = lite_model(conv2d_input=imgs)['dense_3']
    tstop("made predictions")
    # print(f"Model Preds: \n{preds}")
    direction = tf.argmax(preds)[0].numpy()
    direction = (direction+dir_count//2)%dir_count
    # print(f"Pred max: {direction}: {preds[direction]}")
    prev = direction-1 if direction > 0 else dir_count-1
    nxt = direction+1 if direction < dir_count-1 else 0
    next_dirs = [prev,direction,nxt]
    mags = [preds[i][1] for i in next_dirs]
    dirs = [vecs[i] for i in next_dirs]
    go = sum([a*b for a,b in zip(mags, dirs)])/3

    direction = tf.argmax(preds)[0].numpy()
    # print(f"Pred min: {direction}: {preds[direction]}")
    prev = direction-1 if direction > 0 else dir_count-1
    nxt = direction+1 if direction < dir_count-1 else 0
    next_dirs = [prev,direction,nxt]
    mags = [preds[i][0] for i in next_dirs]
    mags = np.exp(mags)/sum(np.exp(mags))
    dirs = [vecs[i] for i in next_dirs]
    avoid = sum([a*b for a,b in zip(mags, dirs)])

    pos = (frac*go-(1-frac)*avoid)
    pos *= 0.25
    pos += 0.5
    return pos

    
    

