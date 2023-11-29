import numpy as np
pos = np.random.random(2)*0.4 + 0.3
def predict(img=None, shape=(2240, 1400)):
    return pos*shape