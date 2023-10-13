import pyautogui
import time
from pymsgbox import *
import threading
from bots import random_bot
from bots import dataset_maker
import os

width, height = pyautogui.size()
# bot = random_bot.newBot()
makeBot = random_bot.newBot
makeRecorderBot = dataset_maker.newDatasetMaker
global bot
global recorderBot


def main():
    response = confirm(text='Click start game after you have entered your name and are ready for the bot to start the game', buttons=['Start bot', 'Cancel'])
    if response == 'Start bot':
        startGame()

def startGame():
    pos = pyautogui.locateCenterOnScreen("play_button.png")
    pyautogui.moveTo(*pos)
    pyautogui.leftClick()
    time.sleep(1)

    global bot
    bot = makeBot()
    global recorderBot
    recorderBot = makeRecorderBot()
    pausablyPlayGame()


def pausablyPlayGame():
    stop_signal = [False]
    play_thread = threading.Thread(target=playGame, args=(stop_signal,))
    play_thread.start()
    alert("Click pause to pause bot", button="Pause")
    stop_signal[0] = True
    pauseBot()

def recordGame(stop_signal):
    delay = 0.5
    id = len(os.listdir("dataset"))
    while not stop_signal[0]:
        start = time.time()
        recorderBot.snap(id)
        id+=1
        duration = time.time()-start
        time.sleep(delay-duration) if duration < delay else None

def playGame(stop_signal):
    delay = 0.1
    while not stop_signal[0]:
        start = time.time()
        bot.nextMove()
        duration = time.time()-start
        time.sleep(delay - duration) if duration < delay else None

def pauseBot():
    stop_signal = [False]
    record_thread = threading.Thread(target=recordGame, args=(stop_signal,))
    record_thread.start()
    response = confirm(text='Click Resume to let the bot take over', buttons=['Resume', 'Kill Bot'])
    stop_signal[0]=True
    if response == 'Resume':
        pausablyPlayGame()


if __name__=='__main__':
    main()
else:
    print(__name__)