# coding: utf-8


import re


class Filter:
    def __init__(self, **rules):
        self.rules = rules

    def match(self, message):
        for field, value in self.rules.items():
            if field not in message or not re.search(value, message[field], re.IGNORECASE):
                return
        return message
