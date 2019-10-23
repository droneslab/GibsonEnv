
class Store(object):
    """Abstract Storage class"""
    def __init__(self):
        super(Store, self).__init__()

    def store(self, key, value):
        pass

    def retrieve(self, key):
        pass


class GPUStore(Store):
    """GPU storage class"""
    def __init__(self):
        super(GPUStore, self).__init__()

    def store(self, key, value):
        pass

    def retrieve(self, key):
        pass


class RAMStore(Store):
    """RAM storage class"""
    def __init__(self):
        super(RAMStore, self).__init__()

    def store(self, key, value):
        pass

    def retrieve(self, key):
        pass


class SSDStore(Store):
    """SSD storage class"""
    def __init__(self):
        super(SSDStore, self).__init__()

    def store(self, key, value):
        pass

    def retrieve(self, key):
        pass


class Memoizer(object):
    """Memoize values in GPU, RAM and SSD"""
    def __init__(self):
        self.gpu = None
        self.ram = None
        self.ssd = None

    def get(self, key):
        pass

    def set(self, key, value):
        pass
