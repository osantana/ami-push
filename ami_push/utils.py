# coding: utf-8


import collections


class LRUCacheDict(collections.OrderedDict):
    def __init__(self, max_size=None):
        super().__init__()
        self.max_size = max_size

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        if self.max_size and len(self) > self.max_size:
            # noinspection PyArgumentList
            self.popitem(last=False)
