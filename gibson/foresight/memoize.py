import os
from functools import wraps
import pickle as pkl

class Store(object):
    """Abstract storage class"""
    def __init__(self):
        super(Store, self).__init__()

    def get(self, key):
        pass

    def set(self, key, value):
        pass

    def open(self):
        return self

    def close(self):
        pass

    def __enter__(self):
        return self.open()

    def __exit__(self):
        self.close()


class GPUStore(Store):
    """GPU storage class"""
    def __init__(self):
        super(GPUStore, self).__init__()

    def get(self, key):
        pass

    def set(self, key, value):
        pass


class RAMStore(Store):
    """RAM storage class"""
    def __init__(self):
        super(RAMStore, self).__init__()

    def get(self, key):
        pass

    def set(self, key, value):
        pass


class SSDStore(Store):
    """SSD storage class"""
    def __init__(self, path):
        super(SSDStore, self).__init__()
        self.path = path

    def exists(self, key):
        return os.path.exists(os.path.join(self.path, key))

    def get(self, key):
        result = None
        with open(os.path.join(self.path, key), 'rb') as fh:
            result = pkl.load(fh)
        return result

    def set(self, key, value):
        with open(os.path.join(self.path, key), 'wb') as fh:
            pkl.dump(value, fh)


class Memoize(object):
    """Memoizer for RL training"""
    def __init__(self, path):
        self.ssd = SSDStore(path)

    def __call__(self, func):
        @wraps(func)
        def wrapped(*args):
            result = None
            key = self.generate_key(args[1])
            if self.exists(key):
                result = self.get(key)
            else:
                result = func(*args)
                self.set(key, result)
            return result

        return wrapped

    def generate_key(self, pose):
        position = pose[0] * 100
        return '{:.0f}_{:.0f}_{:.0f}'.format(position[0], position[1], position[2])

    def exists(self, key):
        """Check if key exists in cache

        :key: key used for storage and retrieval
        :returns: True if key exists, False otherwise
        """
        return self.ssd.exists(key)


    def get(self, key):
        """Retrieve the value in cache against key

        :key: key used for storage and retrieval
        :returns: content stored against the key
        """
        return self.ssd.get(key)

    def set(self, key, value):
        """Store the value in cache against key

        :key: key used for storage and retrieval
        :value: content to be stored
        """
        self.ssd.set(key, value)
