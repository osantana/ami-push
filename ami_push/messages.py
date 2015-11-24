# coding: utf-8


import json

from panoramisk.message import Message


class MessageWrapper:
    def __init__(self, message):
        if isinstance(message, str):
            message = Message.from_line(message)
        self.message = message

    def __getattr__(self, item):
        return getattr(self.message, item)

    def __contains__(self, item):
        return item in self.message

    def __getitem__(self, item):
        return self.message[item]

    def json(self):
        return dict(self.message)

    @property
    def keyid(self):
        return self.uniqueid.split(".")[0]
