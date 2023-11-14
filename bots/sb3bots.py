import stable_baselines3 as sb3

from Bot import AsyncBot


class SB3Bot(AsyncBot):
    def __init__(self, model_path, verbose=False):
        super().__init__(verbose=verbose)
        self.model = sb3.PPO.load(model_path)

    def act(self, state):
        action = self.model.predict(state)[0]
        return action