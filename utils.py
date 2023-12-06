from collections import Counter
from math import ceil
import numpy as np
from PIL import Image
import time
import threading
import os
import pandas as pd

def loading_text(text):
    stop_looping=[False]
    def looping_line(s, stop):
        dots = 10
        while not stop():
            print(" "*(len(s)+dots), end='\r')
            for i in range(dots):
                b = s + "."*i
                print(b, end='\r')
                if stop(): break
                time.sleep(0.1)
        print(f"{s}: Done")
    thread = threading.Thread(target=looping_line, args=(text, lambda: stop_looping[0]))
    # def start():
    #     thread.start()
    # def stop():
    #     text.stop=True
    #     thread.join()
    class LoadingText:
        def start(self):
            thread.start()
        def stop(self):
            stop_looping[0]=True
            thread.join()
    return LoadingText()


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
    return focus_dirs(img, [angle])[0]


class Logger:
    def __init__(self, parent_dir = 'runs', active=True) -> None:
        self.parent_dir = parent_dir
        self.pic = 0
        self.active(active)
    def log_img(self, img, user=False, fullpic=None):
        if not self.logging: return
        plus_part = "user" if user else "system"
        self.name = os.path.join(self.parent_dir, self.run)
        if fullpic:
            self.fullpicname = os.path.join(self.name, '.fullpic')
            os.makedirs(self.fullpicname, exist_ok=True)
            self.fullpicname = os.path.join(self.fullpicname, f"{self.pic:0=10}+{plus_part}.png")
            fullpic.save(self.fullpicname)
        self.name = os.path.join(self.name, f"{self.pic:0=10}+{plus_part}.png")
        img.save(self.name)
        self.pic+=1
    def active(self,logging):
        self.logging = logging
        if not self.logging: return
        os.makedirs(self.parent_dir, exist_ok=True)
        self.run = f"{len(list(filter(lambda i: i[0]!='.',os.listdir(self.parent_dir)))):0=5}"
        os.makedirs(os.path.join(self.parent_dir, self.run))
    def trim_end(self, trim_size=2):
        if not self.logging: return
        pics = os.listdir(os.path.join(self.parent_dir, self.run))
        pics = [os.path.join(self.parent_dir, self.run, i) for i in pics]
        delpics = pics[-2:]
        for p in delpics:
            # print(f"Deleting {p}")
            os.remove(p)


def pull_balanced_preds(dfr, count):
    dfr_np = dfr.to_numpy()
    dfr_stat = pd.DataFrame(
        [np.argmax(dfr_np, 0), np.argmin(dfr_np, 0)],
        columns=dfr.columns,
        index=['argmax', 'argmin']
    )
    stat = dfr_stat.T 
    argmax_vals = stat['argmax'].unique()
    count = ceil(count/len(argmax_vals))
    amag = stat.groupby('argmax')
    take = [amag.get_group(i).sample(count) for i in argmax_vals]
    take = pd.concat(take, axis=0).index
    return dfr[take]
