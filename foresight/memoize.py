import os
from functools import wraps

import numpy as np

import pickle as pkl

from foresight.config import foresight_config as config

class Memoize(object):
    """Memoizer for RL training"""
    def __init__(self, path):
        self.ssd = SSDStore(path)
        self.ram = RAMStore()

        self.store = SingleStoragePolicy(self.ssd)
        if config['StoragePolicy'] == 'RAMOnly':
            self.store = SingleStoragePolicy(self.ram)


    def __call__(self, func):

        if config['EnableMemoization'] == False:
            return func

        @wraps(func)
        def wrapped(*args):
            result = None
            key = self.generate_key(args[1])
            result = self.get(key)
            if result is None:
                result = func(*args)
                self.set(key, result)
            return result

        return wrapped

    def generate_key(self, pose):
        position = pose[0] * 1000
        orientation = np.array(pose[1], dtype=np.float64) * 100
        key = '{:.0f}_{:.0f}_{:.0f}_{:.0f}_{:.0f}_{:.0f}_{:.0f}'.format( position[0]
                                                                        , position[1]
                                                                        , position[2]
                                                                        , orientation[0]
                                                                        , orientation[1]
                                                                        , orientation[2]
                                                                        , orientation[3])
        key = key.replace('-', 'M')
        return key

    def get(self, key):
        """Retrieve the value in cache against key

        :key: key used for storage and retrieval
        :returns: content stored against the key
        """
        return self.store.get(key) if self.store.exists(key) else None


    def set(self, key, value):
        """Store the value in cache against key

        :key: key used for storage and retrieval
        :value: content to be stored
        """
        self.store.set(key, value)


class SingleStoragePolicy(object):

    def __init__(self, store):
        self.store = store

    def get(self, key):
        return self.store.get()

    def set(self, key, value):
        self.store.set(key, value)

    def exists(self, key):
        return self.store.exists()


class Store(object):
    """Abstract storage class"""
    def __init__(self):
        super(Store, self).__init__()

    def exists(self, key):
        pass

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


class RAMStore(Store):
    """RAM storage class"""
    def __init__(self):
        super(RAMStore, self).__init__()
        self.storage = dict()

    def count(self):
        return len(self.storage.keys())

    def get(self, key):
        return self.storage[key]

    def set(self, key, value):
        self.storage[key] = value


class GPUStore(Store):
    """GPU storage class"""
    def __init__(self):
        super(GPUStore, self).__init__()

    def get(self, key):
        pass

    def set(self, key, value):
        pass


