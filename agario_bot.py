import numpy as np
import pyautogui
import time
from pymsgbox import *
from bots import RandomBot, DatasetMaker
from enum import Enum
from pynput import keyboard, mouse
from window_utils import find_agario


class STATE(Enum):
    INIT = 0
    PLAYING = 1
    TERMINATE = 2
    READY = 3


class GameSession:
    def __init__(self, bot, recorderBot, mouse_delay=0.1, dt=0.03, window_pos=None) -> None:
        """
        Interactive game session to record and play agario using a bot or manually
        :param bot:
        :param recorderBot:
        :param dt: step duration. Will attempt to record the state of the game every dt seconds
        """
        self.bot = bot
        self.bot.set_game_session(self)
        self.recorderBot = recorderBot
        self.state = STATE.INIT
        self.do_bot_play = False
        self.region = window_pos
        self.width, self.height = window_pos[2:]
        self.mouse_ct = mouse.Controller()
        # RL stuff
        self.episode_id = None
        self.step_idx = None
        self.mouse_delay = mouse_delay
        self.dt = dt
        # Bot actions. Bot will periodically update these from its thread
        # then the main loop will execute them
        self.bot_action = np.random.random(3)
        self.bot_action_time = 0
        # keyboard actions
        self.kb_action = np.zeros(1)  # only one key - space

    def terminate(self):
        print('terminating')
        self.state = STATE.TERMINATE
        self.recorderBot.save_episode()

    def find_start_buttons(self):
        for bt_im in ["play_bt_smol.png", "play_button.png"]:
            pos = pyautogui.locateCenterOnScreen(bt_im, confidence=0.5, region=self.region)
            if pos is not None:
                return pos

    def notify_bot_action(self, x):
        self.bot_action = x
        self.bot_action_time = time.time()
        if self.do_bot_play:
            action = self.bot_action
            action_ = action + 0.5
            abs_pos = (action_[0] * self.width + self.region[0], action_[1] * self.height + self.region[1])
            pyautogui.moveTo(abs_pos[0], abs_pos[1], duration=self.mouse_delay)

    def main(self):
        # handle keyboard inputs
        def on_press(key):
            # terminate
            if key == keyboard.Key.esc:
                self.terminate()
        listener = keyboard.Listener(on_press=on_press,)
        listener.start()
        while self.state != STATE.TERMINATE:
            # do things
            if self.state == STATE.INIT:
                agario_start_button_pos = self.find_start_buttons()
                if agario_start_button_pos is None:
                    alert("Looking for the play button...", timeout=1000)
                else:
                    self.state = STATE.READY

            elif self.state == STATE.READY:
                mode = confirm(text='Choose mode', buttons=['Start Manual Control', 'Start Bot Control', 'Terminate'])
                # double-check that we still have the agario window
                agario_start_button_pos = self.find_start_buttons()
                if agario_start_button_pos is None:
                    alert("lost agario :<", timeout=1000)
                    self.state = STATE.INIT
                if mode == 'Terminate':
                    self.state = STATE.TERMINATE
                elif mode == 'Start Bot Control':
                    pyautogui.moveTo(*agario_start_button_pos)
                    pyautogui.leftClick()
                    self.state = STATE.PLAYING
                    self.recorderBot.reset_episode()
                    self.do_bot_play = True
                elif mode == 'Start Manual Control':
                    self.state = STATE.PLAYING
                    self.recorderBot.reset_episode()

            elif self.state == STATE.PLAYING:
                reward = 0
                start = time.time()
                img = pyautogui.screenshot(region=self.region)
                img = img.resize((224,224))
                # notify bot of the latest state
                self.bot(img)
                # check if we were killed
                done = pyautogui.locateCenterOnScreen("gamover.png", confidence=0.5) is not None
                # TODO: add reward parsing from the last tmp image
                if done:
                    self.state = STATE.INIT
                step_delay = time.time() - start
                # Wait for the rest of the dt
                time.sleep(self.dt - step_delay) if step_delay < self.dt else None
                if self.do_bot_play:
                    action = self.bot_action
                else:
                    mouse_pos = self.mouse_ct.position
                    action = np.array([mouse_pos[0] / self.width, mouse_pos[1] / self.height, self.kb_action[0]])
                # record the last step
                if not self.state == STATE.TERMINATE:
                    self.recorderBot.add_step(img, action, reward=reward, done=done)


if __name__=='__main__':
    window_info = find_agario()
    window_pos = (max(window_info['x']//2, 0), max(window_info['y'], 0), window_info['width'], window_info['height'])
    game = GameSession(RandomBot(), DatasetMaker(), dt=1/30, window_pos=window_pos)
    game.main()