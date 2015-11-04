# coding: utf-8


# noinspection PyShadowingBuiltins
class Handler:
    def __init__(self, filter, action, url=""):
        self.action = action
        self.filter = filter
        self.url = url
