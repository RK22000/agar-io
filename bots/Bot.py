import time

import numpy
import threading


class Bot:
    def __init__(self, deadline=0.05, verbose=False):
        self.deadline = deadline
        self.action_start_time = 0
        self.game_session = None
        self.busy = False
        self.action_calculation_thread = None
        self.verbose = verbose

    def set_game_session(self, game_session):
        self.game_session = game_session

    def act(self, state):
        raise NotImplementedError

    def _thread_action(self, state):
        action = self.act(state)
        self.game_session.notify_bot_action(action)
        self.busy = False

    def __call__(self, x):
        if not self.busy:
            self.busy = True
            self.action_calculation_thread = threading.Thread(target=self._thread_action, args=(x,))
            self.action_calculation_thread.start()
            self.action_start_time = time.time()
        else:
            if time.time() - self.action_start_time > self.deadline:
                late_time = time.time() - self.action_start_time - self.deadline
                if self.verbose: print(f"Still busy, {late_time:.3f}s late for next action")
            else:
                if self.verbose: print("busy")
