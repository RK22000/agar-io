import pyautogui as pag
import time
import os
import threading
from PIL import Image
import numpy as np
import importlib
pag.useImageNotFoundException(False)

def prep_for_round():
    #====================================================
    # Find Play Button on Agar IO start page
    #----------------------------------------------------
    count = 0
    while True:
        count+=1
        if count == 10: pag.hotkey('ctrl','r')
        if count == 20: return False
        box = pag.locateOnScreen('pics\\play.png', confidence=0.9)
        if box is not None:
            break
        print("Go to https://agar.io/")
        time.sleep(1)
    pag.press('f11')
    time.sleep(1)
    box = pag.locateOnScreen('pics\\play.png', confidence=0.8)
    if box is None: 
        pag.press('f11')
        raise Exception("Could not find play button")
    # print(f"located play button at {box}")
    pos = (box.left+box.width/2, box.top+box.height/2)
    pag.moveTo(*pos)
    return True

def run_round(model, cycle_time=0.05, before_act=lambda img:None, after_act=lambda img:None, timeout=float('inf')):
    pag.leftClick() # Click the start button
    time.sleep(1)
    cont_pic = os.path.join("pics", "cont.png")
    play_pic = os.path.join("pics", "play.png")
    game_over = lambda img: pag.locate(cont_pic, img) is not None or pag.locate(play_pic, img) is not None
    run_round.running = True
    def _game_over():
        game_start = time.time()
        tripped = False
        img = pag.screenshot()
        while not game_over(img):
            if time.time()-game_start > timeout and not tripped:
                pag.press("esc")
                tripped=True
            time.sleep(1)
            img = pag.screenshot()

        run_round.running = False
        # print("Stopping game over loop")
    threading.Thread(target=_game_over).start()
    pos = pag.position()
    while run_round.running:

        img = pag.screenshot()
        cycle_start = time.time()
        # cycle_timer = threading.Thread(target=lambda: time.sleep(cycle_time))
        # cycle_timer.start()
        before_act(img)
        act(img, model) if pos == pag.position() else None
        after_act(img)
        pos = pag.position()
        cycle_duration = time.time() - cycle_start
        if cycle_duration < cycle_time:
            time.sleep(cycle_time - cycle_duration)

    pag.press('f11')
    time.sleep(1)
    box=pag.locateOnScreen("pics\\cont.png", confidence=0.8)
    click=True
    if box is None:
        box = pag.locateOnScreen('pics\\play.png', confidence=0.8)
        click=False
    if box is None:
        raise Exception("Could not find continue button nor play button")
    pos = (box.left+box.width/2, box.top+box.height/2)
    pag.moveTo(*pos)
    if click:
        pag.leftClick()
    return True


def act(img: Image, model):
    try:
        pos = model.predict(img.resize((320,200))) * min(pag.size()) * 0.25 + [i/2 for i in pag.size()]
        pag.moveTo(*pos)
    except Exception as e:
        print(e)

    # pred = np.random.random(2)-0.5
    # pred *= min(pag.size())
    # pred += [i/2 for i in pag.size()]

if __name__=='__main__':
    import argparse
    parser = argparse.ArgumentParser("python main2.py", description="This script runs the agar io bot.")
    parser.add_argument("-r", type=int, default=1, help="How many rounds of agar io to play")
    args = parser.parse_args()
    from models import tflite_ensemble
    for round in range(args.r):
        print(f"Round: {round}")
        if prep_for_round():
            run_round(tflite_ensemble)