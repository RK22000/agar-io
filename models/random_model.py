# import tensorflow as tf
# from tensorflow import keras
# from keras import layers
# import os
# import matplotlib.pyplot as plt
# from math import ceil
import numpy as np

def predict(img: np.ndarray):
    return (((np.random.random_sample(2)*0.8)+0.1) * img.shape[:2])[[1,0]]
