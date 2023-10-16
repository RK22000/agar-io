import numpy as np
import pyautogui
import time
from pymsgbox import *
from bots import RandomBot, DatasetMaker
from enum import Enum
import mouse
from pynput import keyboard


class STATE(Enum):
    INIT = 0
    PLAYING = 1
    PAUSED = 2
    TERMINATE = 3
    READY = 4


class GameSession:
    def __init__(self, bot, recorderBot, mouse_delay=0.1, step_duration=0.03, window_pos=None) -> None:
        """
        Interactive game session to record and play agario using a bot or manually
        :param bot:
        :param recorderBot:
        """
        self.bot = bot
        self.recorderBot = recorderBot
        self.state = STATE.INIT
        self.do_record = False
        self.do_bot_play = False
        self.region = window_pos
        self.width, self.height = pyautogui.size() if window_pos is None else window_pos[2:] - window_pos[:2]
        # RL stuff
        self.episode_id = None
        self.step_idx = None
        self.mouse_delay = mouse_delay
        self.step_duration = step_duration

    def terminate(self):
        print('terminating')
        self.state = STATE.TERMINATE

    def toggle_pause(self):
        print("toggle pause")
        if self.state == STATE.PLAYING:
            self.state = STATE.PAUSED
            # finish and save the recorded episode actions, rewards, and timestamps
            if self.do_record:
                self.recorderBot.save_episode()
        elif self.state == STATE.PAUSED:
            self.state = STATE.PLAYING

    def find_start_buttons(self):
        for bt_im in ["play_bt_smol.png", "play_button.png"]:
            pos = pyautogui.locateCenterOnScreen(bt_im)
            if pos is not None:
                return pos

    def main(self):
        # handle keyboard inputs
        def on_press(key):
            # pause
            if key == keyboard.Key.space:
                self.toggle_pause()
            # terminate
            elif key == keyboard.Key.esc:
                self.terminate()
        listener = keyboard.Listener(on_press=on_press,)
        listener.start()
        while self.state != STATE.TERMINATE:
            # do things
            if self.state == STATE.INIT:
                agario_start_button_pos = self.find_start_buttons()
                if agario_start_button_pos is None:
                    alert("Looking for agario...", timeout=1000)
                else:
                    self.state = STATE.READY

            elif self.state == STATE.READY:
                mode = confirm(text='Choose mode', buttons=['Record Human', 'Record Bot', 'Test Bot', 'Terminate'])
                # double-check that we still have the agario window
                agario_start_button_pos = self.find_start_buttons()
                if agario_start_button_pos is None:
                    alert("lost agario :<", timeout=1000)
                    self.state = STATE.INIT
                if mode == 'Terminate':
                    self.state = STATE.TERMINATE
                elif mode == 'Record Bot':
                    pyautogui.moveTo(*agario_start_button_pos)
                    pyautogui.leftClick()
                    self.state = STATE.PLAYING
                    self.recorderBot.reset_episode()
                    self.do_record = True
                    self.do_bot_play = True
                elif mode == 'Record Human':
                    self.state = STATE.PLAYING
                    self.recorderBot.reset_episode()
                    self.do_record = True
                elif mode == 'Test Bot':
                    pyautogui.moveTo(*agario_start_button_pos)
                    pyautogui.leftClick()
                    self.state = STATE.PLAYING
                    self.do_bot_play = True

            elif self.state == STATE.PAUSED:
                mode = confirm(text='Choose mode', buttons=['Resume', 'Terminate'])
                if mode == 'Terminate':
                    self.state = STATE.TERMINATE
                elif mode == 'Resume':
                    self.state = STATE.PLAYING
                    self.recorderBot.reset_episode()

            elif self.state == STATE.PLAYING:
                reward = 0
                start = time.time()
                tmp_img_name = "tmp.png"
                img = pyautogui.screenshot(tmp_img_name, region=self.region)
                if self.do_bot_play:
                    action = self.bot(img)
                    print("action", action)
                    action_ = action + 0.5
                    abs_pos = (action_[0] * self.width, action_[1] * self.height)
                    pyautogui.moveTo(abs_pos[0], abs_pos[1], duration=self.mouse_delay)
                else:
                    abs_pos = mouse.get_position()
                    action = np.array((abs_pos[0] / self.width, abs_pos[1] / self.height))
                # check if we were killed
                done = pyautogui.locateCenterOnScreen("gamover.png") is not None
                # TODO: add reward parsing from the last tmp image
                if done:
                    self.state = STATE.INIT
                if self.do_record:
                    self.recorderBot.add_step(action, reward=reward, done=done, tmp_img_name=tmp_img_name)
                decision_making_delay = time.time() - start
                time.sleep(self.step_duration - decision_making_delay) if decision_making_delay < self.step_duration else None


if __name__=='__main__':
    # todo: find correct agario window position/size
    window_pos = np.array((0,0, 1920, 1080), dtype=np.int32)
    game = GameSession(RandomBot(), DatasetMaker(), window_pos=window_pos)
    game.main()