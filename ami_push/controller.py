# coding: utf-8
import asyncio

from filters import Filter
from handlers import Handler
from utils import LRUCacheDict


DEFAULT_MAX_QUEUES = 100
DEFAULT_MAX_QUEUE_SIZE = 100


class Controller:
    def __init__(self, loop=None, max_queues=DEFAULT_MAX_QUEUES, max_queue_size=DEFAULT_MAX_QUEUE_SIZE):
        if loop is None:
            loop = asyncio.get_event_loop()
        self.loop = loop
        self.max_queue_size = max_queue_size
        self.queues = LRUCacheDict(max_queues)
        self.filters = {}
        self.handlers = []

    def load_configs(self, filters, handlers):
        for name, filter_ in filters.items():
            self.filters[name] = Filter(**filter_)

        for handler in handlers:
            self.handlers.append(Handler(**handler))

    def handle(self, message):
        for handler in self.handlers:
            handler.handle(self, message)
