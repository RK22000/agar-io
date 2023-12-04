from collections import Counter
from math import ceil
import numpy as np
from PIL import Image
import time


def tstart():
    global t
    t = time.time()
def tstop(s):
    global t
    print(f"{s}: {time.time()-t}")
    tstart()

def focus_dirs(img, angles):
    '''Focus the POV of the image towards a certain directions
    Takes in a PIL image and angle in degrees
    Returns an image with the center shifted to the left and the image rotated so the angle direction is to the right
    The fill values after rotation are based on the edge values'''
    colors = Counter(img.getdata())
    color = max(colors, key=lambda i: colors[i])
    color = np.asarray(color).astype(np.uint8)
    w,h = img.size
    d = ceil(np.linalg.norm(img.size))
    img_arr = np.asarray(img)
    # del(img)
    top = img_arr[0]
    bot = img_arr[-1]
    lef = img_arr[:,0]
    rig = img_arr[:,-1]
    s0 = (d-h)//2
    s1 = (d-w)//2
    
    big = np.array([[color]*d]*d)
    # print(big.dtype)
    big[s0:s0+h, 0:s1] = np.stack([lef]*s1, axis=1)
    big[s0:s0+h, s1+w:] = np.stack([rig]*(d-s1-w), axis=1)
    big[0:s0, s1:s1+w] = np.stack([top]*s0)
    big[s0+h:, s1:s1+w] = np.stack([bot]*(d-s0-h))
    big[s0:s0+h, s1:s1+w] = img_arr
    # del(img_arr)
    img2 = Image.fromarray(big)
    # del(big)
    return [img2.rotate(angle).crop((s1+w/3, s0, s1+w, s0+h)) for angle in angles]
    

def focus_dir(img, angle):
    '''Focus the POV of the image towards a certain direction
    Takes in a PIL image and angle in degrees
    Returns an image with the center shifted to the left and the image rotated so the angle direction is to the right
    The fill values after rotation are based on the edge values'''
    colors = Counter(img.getdata())
    color = max(colors, key=lambda i: colors[i])
    color = np.asarray(color).astype(np.uint8)
    w,h = img.size
    d = ceil(np.linalg.norm(img.size))
    img_arr = np.asarray(img)
    del(img)
    top = img_arr[0]
    bot = img_arr[-1]
    lef = img_arr[:,0]
    rig = img_arr[:,-1]
    s0 = (d-h)//2
    s1 = (d-w)//2
    big = np.array([[color]*d]*d)
    # print(big.dtype)
    big[s0:s0+h, 0:s1] = np.stack([lef]*s1, axis=1)
    big[s0:s0+h, s1+w:] = np.stack([rig]*(d-s1-w), axis=1)
    big[0:s0, s1:s1+w] = np.stack([top]*s0)
    big[s0+h:, s1:s1+w] = np.stack([bot]*(d-s0-h))
    big[s0:s0+h, s1:s1+w] = img_arr
    del(img_arr)
    img2 = Image.fromarray(big)
    del(big)
    return img2.rotate(angle).crop((s1+w/3, s0, s1+w, s0+h))
    