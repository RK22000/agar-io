import utils
t = utils.loading_text("Loading imports")
t.start()
import time
import threading
import pyautogui as pyg
import numpy as np
import os
import models.model_experiemnt_lab as model
import importlib
import sys
from math import atan2
import traceback
import pandas as pd
t.stop()

logging_dir = "runs3"
os.makedirs(logging_dir, exist_ok=True)
one_run_mode = True

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
    if box is None: 
        pyg.press('f11')
        return False
    print(f"located play button at {box}")
    pos = (box.left+box.width/2, box.top+box.height/2)
    pyg.moveTo(*pos)

    #====================================================
    # Instantiate the logger
    #----------------------------------------------------
    logger = utils.Logger(parent_dir=logging_dir, active=not one_run_mode)


    #====================================================
    # Start and play Agar IO Game
    #----------------------------------------------------
    screen_shape = np.asarray(pyg.size())
    pic = 0
    pyg.leftClick()
    time.sleep(0.5)
    while pyg.locateOnScreen("pics\\cont_button.png") is None and pyg.locateOnScreen('pics\\play_button.png') is None:
        pos = pyg.position()

        # Capture image
        img = pyg.screenshot()
        w,h = img.size
        n = 200
        w = w*n//h
        h = n
        im = img.resize((w,h))

        time.sleep(0.0005)

        user_played = pos != pyg.position()
        if user_played: # Player is interacting with the mouse. Let them play
            pos = pyg.position()
            # print(f"player played to {pos}")
            # name = os.path.join(parent_dir, run, f"{pic:0=10}+user.png")
            # pic+=1
            # continue
        else: #<<< Use model to pick next coordinates
            s = time.time()
            pos = model.predict(im) * screen_shape
            # print(f"Prediction wait: {time.time()-s} seconds")
            # print(f"System playing to {pos}")
            pyg.moveTo(*pos)
            # name = os.path.join(parent_dir, run, f"{pic:0=10}+system.png")
            # pic+=1
        # x = pos[0] - screen_shape[0]/2
        # y = pos[1] - screen_shape[1]/2
        x,y = pos - screen_shape/2
        # angle = atan2(y,x) * 180 / np.pi
        # im = utils.focus_dir(im, angle)
        # logger.log_img(im, user_played,img)
        if False and pic >= 100:
            pyg.press('esc')

    pyg.press('f11')
    # pics = os.listdir(os.path.join(parent_dir, run))
    # pics = [os.path.join(parent_dir, run, i) for i in pics]
    # delpics = pics[-2:]
    # for p in delpics:
    #     # print(f"Deleting {p}")
    #     os.remove(p)
    # logger.trim_end(2)
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

df_name = "rounds.csv"
if os.path.exists(df_name):
    df = pd.read_csv(df_name, index_col=False)
else:
    df = pd.DataFrame(columns=['Model', 'Survival_Time', 'Reaction_Time', 'Run_Dir', 'Error'])

good_rounds = []
bad_rounds = []
round = len(os.listdir(logging_dir))
roundLim = round + 500
frac_n = 5
fracs = [i/(frac_n-1) for i in range(frac_n)]
students = [
 'student_models\\sum_normal_e09.keras',
 'student_models\\0.05_e09.keras',
 'student_models\\0.1_e09.keras',
 'student_models\\1.5_e09.keras',
 'student_models\\0.5_e09.keras'
 'student_models\\1_e09.keras',
]
while round < roundLim:
    importlib.reload(model)
    i = round%frac_n
    model_name = f"go{int(fracs[i]*100)}-avoid{int((1-fracs[i])*100)}"
    i = round%len(students)
    model_name = students[i][15:-6]
    model_name = "bull_model"
    print(f"start of round: {round}/{model_name}")
    # model.load_student(students[i])
    res = False
    stop=False
    def cap():
        count = 0
        while not stop and count < 20*60/1:
            count+=1
            time.sleep(1)
        pyg.press('esc')
    timer = threading.Thread(target=cap)
    try:
        # model.frac=fracs[i]
        # model.reset_reaction_time()
        timer.start()
        start_time = time.time()
        res = one_round()
        end_time = time.time()
        stop=True
    except Exception as e:
        end_time = time.time()
        stop=True
        print(f"Exception in round {round}")
        print(traceback.format_exc())
    timer.join()
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
        pyg.hotkey('ctrl','r')
    stats = [model_name, end_time-start_time, model.react_time/model.react_count, os.path.join(logging_dir, f"{round:0=5}"), not res]
    print(f"Stats: {stats}")
    print(f"end of round: {round}/{model_name}: {end_time-start_time} seconds")
    if not one_run_mode:
        df.loc[len(df)] = stats
        df.to_csv(df_name, index=False)
        pass
    if not res and one_run_mode:
        # sys.exit(0)
        break
        pass
    round+=1
    time.sleep(1)

print("Exiting script")