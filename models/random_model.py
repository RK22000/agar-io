import numpy as np

name="random-model"
def predict(img: np.ndarray):
    pos = np.random.random(2)
    pos = pos/np.linalg.norm(pos)
    return pos
