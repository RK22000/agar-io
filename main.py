import pyautogui as pyg
import time
import numpy as np
import os
import models.random_model as model
import sys

#====================================================
# Find Play Button on Agar IO start page
#----------------------------------------------------
while True:
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
# Instantiate imitation learning model
#----------------------------------------------------

#====================================================
# Start and play Agar IO Game
#----------------------------------------------------
pyg.leftClick()

dataset_size = int(os.listdir('data_imitation')[-1].split('-')[0]) if os.listdir('data_imitation') else 0
while (box:=pyg.locateOnScreen("pics\\cont_button.png")) is None:
    pos = pyg.position()
    im = pyg.screenshot()
    time.sleep(1)
    if pos != pyg.position(): # Player is interacting with the mouse. Let them play
        pos = pyg.position()
        print(f"player played to {pos}")
        name = f"data_imitation\\{dataset_size:0=10}-{pos[0]}x{pos[1]}.png"
        im.save(name)
        dataset_size+=1
        continue
    #### Current method of setting next coordinate
    # pos = np.random.random_sample(2) * pyg.size()
    ####
    #<<< Use model to pick next coordinates
    pos = model.predict(np.array(pyg.screenshot()))
    #??? Should the code over here trigger next round of training on model
    #??? Or should the code in the model decide the appropriate time to do 
    #??? that

    #<<<
    print(f"System playing to {pos}")
    pyg.moveTo(*pos, 0.3)

pyg.press('f11')
time.sleep(1)
box=pyg.locateOnScreen("pics\\cont_button.png")
pos = (box.left+box.width/2, box.top+box.height/2)
pyg.moveTo(*pos)


