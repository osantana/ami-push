# coding: utf-8


import asyncio
import logging

from panoramisk import Manager

from .controller import Controller, DEFAULT_MAX_QUEUES, DEFAULT_MAX_QUEUE_SIZE
from .messages import MessageWrapper


class Bridge:
    def __init__(self, options, filters, push_configs):
        self.loop = asyncio.get_event_loop()

        max_queues = options.pop("max_size", DEFAULT_MAX_QUEUES)
        max_queue_size = options.pop("max_queue_size", DEFAULT_MAX_QUEUE_SIZE)
        self.controller = Controller(self.loop, max_queues, max_queue_size)
        self.controller.load_configs(filters, push_configs)

        options.pop("loop", None)  # discard invalid argument
        self.manager = Manager(loop=self.loop, **options)
        self.manager.log.addHandler(logging.NullHandler())
        self.manager.register_event("*", self.handle_events)

    @asyncio.coroutine
    def handle_events(self, manager, message):
        wrapper = MessageWrapper(message)
        yield from self.controller.handle(wrapper)

    @asyncio.coroutine
    def connect(self):
        yield from self.manager.connect()

    def run(self):
        try:
            self.loop.run_until_complete(self.connect())
            self.loop.run_forever()
        finally:
            self.loop.close()
