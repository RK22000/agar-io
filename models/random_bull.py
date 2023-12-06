import numpy as np
pos = np.random.random(2)*0.4 + 0.3

react_time=0
react_count=0.000001
def reset_reaction_time():
    global react_time, react_count
    react_time=0
    react_count=0.000001
    
def predict(img=None):
    return pos