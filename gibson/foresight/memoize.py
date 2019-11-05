import os
from functools import wraps

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

    def get(self, key):
        result = None
        with open(os.path.join(self.path, key), 'r') as fh:
            result = fh.read()
        return result

    def set(self, key, value):
        with open(os.path.join(self.path, key), 'w') as fh:
            fh.write(value)


class Memoize(object):
    """Memoizer for RL training"""
    def __init__(self, path):
        self.ssd = SSDStore(path)

    def __call__(self, func):
        @wraps(func)
        def wrapped(*args):
            return func(*args)

        return wrapped

    def get(self, key):
        """Retrieve the value in cache against key

        :key: key used for storage and retrieval
        :returns: content stored against the key
        """
        self.ssd.get(key)

    def set(self, key, value):
        """Store the value in cache against key

        :key: key used for storage and retrieval
        :value: content to be stored
        """
        self.ssd.set(key)
