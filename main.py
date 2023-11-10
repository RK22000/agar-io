import pyautogui as pyg
import time
import numpy as np

#====================================================
# Find Play Button on Agar IO start page
#----------------------------------------------------
while True:
    box = pyg.locateOnScreen('pics\\play_button.png')
    if box is not None:
        break
    print("Go to https://agar.io/")
    time.sleep(1)
print(f"located play button at {box}")
pos = (box.left+box.width/2, box.top+box.height/2)
pyg.moveTo(*pos)

#====================================================
# Start and play Agar IO Game
#----------------------------------------------------
pyg.leftClick()
while (box:=pyg.locateOnScreen("pics\\cont_button.png")) is None:
    pos = pyg.position()
    time.sleep(1)
    if pos != pyg.position(): # Player is interacting with the mouse. Let them play
        print("player played")
        continue
    pos = np.random.random_sample(2) * pyg.size()
    print(f"System playing to {pos}")
    pyg.moveTo(*pos)

pos = (box.left+box.width/2, box.top+box.height/2)
pyg.moveTo(*pos)


