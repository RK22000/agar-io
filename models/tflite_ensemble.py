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
prev_pos = np.array((0,0))

name='tflite-ensemble'
def predict(img):
    expected_size = (320,200)
    assert img.size == expected_size, f"Prediction can only be made on images of size {expected_size}. Got image of size {img.size}"
    imgs = utils.focus_dirs(img, angles)
    imgs = np.asarray(imgs, np.float32)/255
    preds = lite_model(conv2d_input=imgs)['dense_3']

    mags = preds[:,0] - 0.5
    mags = (mags > 0) * mags
    T = 0.1
    mags = np.exp(mags/T)/sum(np.exp(mags/T))
    dirs = vecs
    pos = -sum([a*b for a,b in zip(mags, dirs)])*2
    f = 0.9
    global prev_pos
    pos = f*pos + (1-f)*prev_pos
    prev_pos = pos
    return pos


def many_preds(imgs):
    '''predict on a list of images'''
    start_img_len = len(imgs)
    imgss = [utils.focus_dirs(im, angles) for im in imgs]
    imgss = [np.asarray(imgs, np.float32) for imgs in imgss]
    imgs = np.concatenate(imgss)/255
    preds = lite_model(conv2d_input=imgs)['dense_3']
    preds = np.reshape(preds, (start_img_len, 6, 2))