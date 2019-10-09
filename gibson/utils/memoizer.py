import gym
from gym.core import Wrapper

from gibson.utils.monitor import Monitor


class Memoizer(Monitor):

    def __init__(self, env, filename, allow_early_resets=False, reset_keywords=()):
        print('Memoizer.__init__')
        Monitor.__init__(self, env=env, filename=filename, allow_early_resets=allow_early_resets, reset_keywords=reset_keywords)

    def render_observations(self, pose):
        print('Memoizer.render_observations | pose: {}'.format(pose))
        return self.env.render_observations(pose)
