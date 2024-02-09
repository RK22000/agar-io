import pyautogui as pyg
import time
import numpy as np
import os
import models.model_experiemnt_lab as model
import importlib
import sys
import utils
from math import atan2
import traceback


def one_round():
    #====================================================
    # Find Play Button on Agar IO start page
    #----------------------------------------------------
    count = 0
    while True:
        count+=1
        if count >= 10: return False
        box = pyg.locateOnScreen('pics\\play_button.png')
        if box is not None:
            break
        print("Go to https://agar.io/")
        time.sleep(1)
    pyg.press('f11')
    time.sleep(1)
    box = pyg.locateOnScreen('pics\\play_button.png')
    print(f"located play button at {box}")
    pos = (box.left+box.width/2, box.top+box.height/2)
    pyg.moveTo(*pos)

    #====================================================
    # Instantiate directory to record run
    #----------------------------------------------------
    parent_dir = "runs"
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)
    run = f"{len(os.listdir(parent_dir)):0=5}"
    os.makedirs(os.path.join(parent_dir, run))


    #====================================================
    # Start and play Agar IO Game
    #----------------------------------------------------
    screen_shape = pyg.size()
    pic = 0
    pyg.leftClick()
    time.sleep(0.5)
    while pyg.locateOnScreen("pics\\cont_button.png") is None and pyg.locateOnScreen('pics\\play_button.png') is None:
        pos = pyg.position()

        # Capture image
        im = pyg.screenshot()
        w,h = im.size
        n = 200
        w = w*n//h
        h = n
        im = im.resize((w,h))

        time.sleep(0.0005)

        if pos != pyg.position(): # Player is interacting with the mouse. Let them play
            pos = pyg.position()
            print(f"player played to {pos}")
            name = os.path.join(parent_dir, run, f"{pic:0=10}+user.png")
            pic+=1
            # continue
        else: #<<< Use model to pick next coordinates
            s = time.time()
            pos = model.predict(im) * screen_shape
            print(f"Prediction wait: {time.time()-s} seconds")
            #??? Should the code over here trigger next round of training on model
            #??? Or should the code in the model decide the appropriate time to do 
            #??? that
            #<<<
            print(f"System playing to {pos}")
            pyg.moveTo(*pos)
            name = os.path.join(parent_dir, run, f"{pic:0=10}+system.png")
            pic+=1
        x = pos[0] - screen_shape[0]/2
        y = pos[1] - screen_shape[1]/2
        angle = atan2(y,x) * 180 / np.pi
        utils.focus_dir(im, angle).save(name)
        if False and pic >= 100:
            pyg.press('esc')

    pyg.press('f11')
    pics = os.listdir(os.path.join(parent_dir, run))
    pics = [os.path.join(parent_dir, run, i) for i in pics]
    delpics = pics[-2:]
    for p in delpics:
        # print(f"Deleting {p}")
        os.remove(p)
    time.sleep(1)
    box=pyg.locateOnScreen("pics\\cont_button.png")
    click=True
    if box is None:
        box = pyg.locateOnScreen('pics\\play_button.png')
        click=False
    pos = (box.left+box.width/2, box.top+box.height/2)
    pyg.moveTo(*pos)
    if click:
        pyg.leftClick()
    return True


good_rounds = []
bad_rounds = []
round = len(os.listdir('runs'))
roundLim = round + 500
while round < roundLim:
    print(f"start of round: {round}")
    res = False
    try:
        importlib.reload(model)
        res = one_round()
    except Exception as e:
        print(f"Exception in round {round}")
        print(traceback.format_exc())
    if res:
        good_rounds.append(round)
    else:
        bad_rounds.append(round)
        name = f"erpics\\{round:0=5}.png"
        n=0
        while os.path.exists(name):
            n+=1
            name = f"{name[:-4]}({n}).png"
        pyg.screenshot().save(name)
    print(f"end of round: {round}")
    round+=1
    time.sleep(1)

