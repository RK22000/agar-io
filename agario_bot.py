import os

import cv2
import numpy as np
import pyautogui
import time

from PIL import Image
from pymsgbox import *
from bots import RandomAsyncBot, RandomSyncBot, DatasetMaker
from enum import Enum
from pynput import keyboard, mouse
import pytesseract
import gymnasium as gym
import webbrowser
from mss import mss

from window_utils import find_agario


class STATE(Enum):
    INIT = 0
    PLAYING = 1
    TERMINATE = 2
    READY = 3
    RESTART = 4


def parse_score(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    bw = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)[1]
    text = pytesseract.image_to_string(bw)
    print(text)
    start = text.find('food eaten highest mass')
    text_s = text[start:].split('\n')
    food_eaten = float(text_s[1].split(' ')[0])
    start = text.find('cells eaten top position')
    text_s = text[start:].split('\n')
    cells_eaten = float(text_s[1].split(' ')[0])
    return food_eaten, cells_eaten


def find_img(img, target, reg=None, absolute=False, threshold=.5):
    res = cv2.matchTemplate(img, target, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    if len(loc[0]) > 0:
        if absolute:
            return loc[1][0] + reg['left'] + target.shape[0]//2, loc[0][0] + reg['top'] + target.shape[1]//2
        else:
            return loc[1][0], loc[0][0]


class Agarioenv(gym.core.Env):
    AGARIO_URL = 'https://agar.io/'
    def __init__(self, dt=0.03) -> None:
        """
        Interactive game session to record and play agario using a bot or manually
        :param bot:
        :param recorderBot:
        :param dt: step duration. Will attempt to record the state of the game every dt seconds
        """
        try:
            # see if the agario window is already open
            window_info = find_agario()
        except:
            # open a new window otherwise
            webbrowser.open_new(Agarioenv.AGARIO_URL)
            # wait for the website to load
            for i in range(10):
                try:
                    window_info = find_agario()
                    break
                except Exception as e:
                    print('failed to find agario window')
                    time.sleep(1)
        print(window_info)
        self.state = STATE.INIT
        self.do_bot_play = False
        self.reg = window_info
        self.regarr = np.array([window_info['left'], window_info['top'], window_info['width'], window_info['height']])
        self.mouse_ct = mouse.Controller()
        # RL stuff
        self.episode_id = None
        self.step_idx = None
        self.dt = dt
        self.clock = time.time()
        self.action_space = gym.spaces.Box(low=0, high=1, shape=(3,), dtype=np.float32)
        self.observation_space = gym.spaces.Box(low=0, high=255, shape=(224, 224, 3), dtype=np.uint8)
        # Bot actions. Bot will periodically update these from its thread
        # then the main loop will execute them
        self.bot_action = self.action_space.sample()
        self.bot_action_time = 0
        # keyboard actions
        self.kb_action = np.zeros(1)  # only one key - space
        # handle keyboard inputs
        def on_press(key):
            # terminate
            if key == keyboard.Key.esc:
                self.terminate()
            if key == keyboard.Key.space:
                self.bot_action[2] = 1.0
            if key == keyboard.Key.shift_l:
                self.toggle_bot_play()
        self.listener = keyboard.Listener(on_press=on_press, )
        self.listener.start()
        self.sct = mss()
        self.playbt = cv2.imread('play_bt_smol.png')
        self.gmover = cv2.imread('gameover.png')
        self.contbt = cv2.imread('cont_button.png')
        self.popupsolution = cv2.imread('popupweakspot.png')

    def terminate(self):
        print('terminating')
        self.state = STATE.TERMINATE

    def find_start_buttons(self, absolute=False):
        sct_img = self.sct.grab(self.reg)
        img_rgb = np.array(sct_img)[:, :, :-1]
        return find_img(img_rgb, self.playbt, self.reg, absolute=absolute)

    def notify_bot_action(self, x):
        self.bot_action = x
        self.bot_action_time = time.time()
        if self.do_bot_play:
            action_ = self.bot_action
            abs_pos = (action_[0] * self.reg['width'] + self.reg['left'], action_[1] * self.reg['height'] + self.reg['top'])
            pyautogui.moveTo(abs_pos[0], abs_pos[1])
            if action_[2] > 0.9:
                pyautogui.keyDown('space')
                pyautogui.keyUp('space')

    def toggle_bot_play(self):
        self.do_bot_play = not self.do_bot_play
        print(f"bot play: {self.do_bot_play}")

    def reset(self, manual=False):
        self.state = STATE.INIT
        while not self.state == STATE.PLAYING:
            if self.state == STATE.INIT:
                agario_start_button_pos = self.find_start_buttons(absolute=True)
                if agario_start_button_pos is None:
                    alert("Looking for the play button...", timeout=100)
                    # maybe blocked by a popup?
                    sct_img = self.sct.grab(self.reg)
                    img_rgb = np.array(sct_img)[:, :, :-1]
                    xy = find_img(img_rgb, self.popupsolution, self.reg, absolute=True)
                    if xy is not None:
                        print("found popup, closing it")
                        pyautogui.moveTo(*xy)
                        pyautogui.leftClick()
                else:
                    self.state = STATE.READY
            elif self.state == STATE.RESTART:
                # find the continue button
                sct_img = self.sct.grab(self.reg)
                img_rgb = np.array(sct_img)[:, :, :-1]
                xy = find_img(img_rgb, self.contbt, self.reg, absolute=True)
                if xy is None:
                    alert("Looking for the continue button...", timeout=100)
                else:
                    pyautogui.moveTo(*xy)
                    pyautogui.leftClick()
                    self.state = STATE.INIT
            elif self.state == STATE.READY:
                if manual:
                    mode = confirm(text='Choose mode', buttons=['Start Manual Control', 'Start Bot Control', 'Terminate'])
                else:
                    mode = 'Start Bot Control'
                # double-check that we still have the agario window
                agario_start_button_pos = self.find_start_buttons(absolute=True)
                if agario_start_button_pos is None:
                    alert("lost agario :<", timeout=1000)
                    self.state = STATE.INIT
                if mode == 'Terminate':
                    self.state = STATE.TERMINATE
                elif mode == 'Start Bot Control':
                    pyautogui.moveTo(*agario_start_button_pos)
                    pyautogui.leftClick()
                    self.state = STATE.PLAYING
                    self.do_bot_play = True
                    time.sleep(2.0)
                elif mode == 'Start Manual Control':
                    self.state = STATE.PLAYING
        # reset the realtime clock
        self.clock = time.time()
        self.step_idx = 0
        return self.step(self.action_space.sample())[0]

    def step(self, action):
        self.notify_bot_action(action)
        reward = 0
        # wait for the rest of the dt if needed to maintain framerate
        step_delay = time.time() - self.clock
        print(f"step delay: {step_delay:.3f}s")
        if step_delay < self.dt:
            time.sleep(self.dt - step_delay)
        self.clock = time.time()
        img = self.sct.grab(self.reg)
        if self.step_idx % 5 == 0:
            done = find_img(np.array(img)[:, :, :-1], self.gmover, self.reg, threshold=0.9) is not None
        else:
            done = False
        img = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")
        img = img.resize((224, 224))
        # check if we were killed
        # this takes an average of 0.31s
        if done:
            self.state = STATE.RESTART
            # parse the score, attempt 10 times
            sfood, scells = 0, 0
            for i in range(100):
                try:
                    xmargin = int(self.rec['width'] // 2.5)
                    ymargin = self.rec['height'] // 8
                    _bb = {
                        'top': self.rec['top'] + ymargin,
                        'left': self.rec['left'] + xmargin,
                        'width': self.rec['width'] - 2 * xmargin,
                        'height': self.rec['height'] - 4 * ymargin,
                    }
                    cropped_img = self.sct.grab(_bb)
                    sfood, scells = parse_score(np.array(cropped_img)[:, :, :-1])
                except Exception as e:
                    print(e)
            print(f"score: {sfood} food eaten, {scells} cells eaten")
            reward = sfood + scells
        self.step_idx += 1
        return img, reward, done, None, None

    def main(self, bot, recorderBot):
        while self.state != STATE.TERMINATE:
            if self.state == STATE.INIT or self.state == STATE.RESTART:
                obs = self.reset(manual=True)
                recorderBot.reset_episode()

            elif self.state == STATE.PLAYING:
                action = bot(np.array(obs)[:, :, :-1])
                obs, rew, term, trun, _ = self.step(action)
                if self.do_bot_play:
                    action = self.bot_action
                else:
                    mouse_pos = self.mouse_ct.position
                    action = np.array([mouse_pos[0] / self.reg['width'], mouse_pos[1] / self.reg['height'], self.kb_action[0]])
                recorderBot.add_step(obs, action, reward=rew, done=term)
        recorderBot.save_episode()


if __name__=='__main__':
    os.environ['TESSDATA_PREFIX'] = os.curdir
    game = Agarioenv(dt=1/30)
    bot, ds = RandomSyncBot(), DatasetMaker()
    game.main(bot, ds)
