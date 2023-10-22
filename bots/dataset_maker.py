import time

import numpy as np
import os
import random as rnd


class DatasetMaker:
    def __init__(self, root="dataset", max_ep_len=512, use_max_ep_len=True) -> None:
        if not os.path.isdir(root):
            os.makedirs(root)
        self.root = root
        self.episode_id = None
        self.step_idx = None
        self.max_ep_len = max_ep_len
        self.use_max_ep_len = use_max_ep_len
        self.ep_actions = None
        self.ep_rewards = None
        self.ep_timestamps = None

    def reset_episode(self):
        print("resetting episode")
        self.episode_id = rnd.randint(0, int(2 ** 32))
        self.step_idx = 0
        self.ep_actions = np.zeros((512, 2))
        self.ep_rewards = np.zeros(512)
        self.ep_timestamps = np.zeros(512)

    def save_episode(self):
        print("saving episode")
        # truncate and save the episode
        self.ep_actions = self.ep_actions[:self.step_idx]
        self.ep_rewards = self.ep_rewards[:self.step_idx]
        self.ep_timestamps = self.ep_timestamps[:self.step_idx]
        np.savez(os.path.join(self.root, f"{self.episode_id}.npz"), actions=self.ep_actions, rewards=self.ep_rewards, timestamps=self.ep_timestamps)

    def add_step(self, img, action, reward, done):
        self.ep_actions[self.step_idx] = action
        self.ep_rewards[self.step_idx] = reward
        self.ep_timestamps[self.step_idx] = time.time()
        img_name = f"{self.episode_id}_{self.step_idx}.png"
        img.save(os.path.join(self.root, img_name))
        if done:
            self.save_episode()
            self.reset_episode()
        else:
            self.step_idx += 1
            # check if episode is too long
            if self.step_idx >= 512:
                if self.use_max_ep_len:
                    self.save_episode()
                    self.reset_episode()
                else:
                    # extend the array if the maximum length is not enforced
                    self.ep_actions = np.concatenate((self.ep_actions, np.zeros((512, 2))))
                    self.ep_rewards = np.concatenate((self.ep_rewards, np.zeros(512)))
                    self.ep_timestamps = np.concatenate((self.ep_timestamps, np.zeros(512)))