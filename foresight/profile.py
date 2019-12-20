from profilehooks import profile

from foresight.config import foresight_config as config


class Profile(object):
    """Memoizer for RL training"""
    def __init__(self, filename=None):
        self.filename = config['Profile']['Filename'] if filename is None else filename

    def __call__(self, func):
        if config['Profile']['Enabled'] is True:
            filename = self.filename.format(func.__name__)
            return profile(func, filename=filename)
        else:
            return func
