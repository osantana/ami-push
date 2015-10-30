# coding: utf-8


import asyncio
import logging

from panoramisk import Manager

from .message import MessageWrapper
from .utils import LRUCacheDict

DEFAULT_MAX_QUEUES = 100
DEFAULT_MAX_QUEUE_SIZE = 100


class Rule:
    def __init__(self, **options):
        pass

    def match(self, message):
        return self


class Controller:
    def __init__(self, loop=None, max_queues=DEFAULT_MAX_QUEUES, max_queue_size=DEFAULT_MAX_QUEUE_SIZE):
        if loop is None:
            loop = asyncio.get_event_loop()
        self.loop = loop
        self.max_queue_size = max_queue_size
        self.queues = LRUCacheDict(max_queues)
        self.rules = []

    def load_rules(self, rules):
        for rule_options in rules:
            self.rules.append(Rule(**rule_options))

    def handle(self, message):
        rules = []
        for rule in self.rules:
            match = rule.match(message)
            if match:
                self.process(match, message)

    def process(self, match, message):
        pass


class Bridge:
    def __init__(self, options, rules):
        self.loop = asyncio.get_event_loop()

        max_queues = options.pop("max_size", DEFAULT_MAX_QUEUES)
        max_queue_size = options.pop("max_queue_size", DEFAULT_MAX_QUEUE_SIZE)
        self.controller = Controller(self.loop, max_queues, max_queue_size)
        self.controller.load_rules(rules)

        options.pop("loop", None)  # discard invalid argument
        self.manager = Manager(loop=self.loop, **options)
        self.manager.log.addHandler(logging.NullHandler())
        self.manager.register_event("*", self.handle_events)

    def handle_events(self, manager, message):
        wrapper = MessageWrapper(message)
        self.controller.handle(wrapper)

    @asyncio.coroutine
    def connect(self):
        yield from self.manager.connect()

    def run(self):
        try:
            self.loop.run_until_complete(self.connect())
            self.loop.run_forever()
        finally:
            self.loop.close()
