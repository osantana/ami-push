# coding: utf-8


import asyncio

from ami_push.filters import Filter
from ami_push.pusher import Pusher
from ami_push.utils import LRUCacheDict

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
        self.pushers = []

    def load_configs(self, filters, push_configs):
        for name, filter_ in filters.items():
            self.filters[name] = Filter(**filter_)

        for push_config in push_configs:
            self.pushers.append(Pusher(**push_config))

    def _enqueue(self, message):
        queue = self.queues.setdefault(message.keyid, asyncio.Queue(maxsize=self.max_queue_size))
        try:
            queue.put_nowait(message)
            return queue
        except asyncio.QueueFull:
            # TODO: log discarded info
            return queue

    def handle(self, message):
        for name, filter_ in self.filters.items():
            if not filter_.match(message):
                continue

            queue = self._enqueue(message)

            for pusher in self.pushers:
                if name not in pusher.filter:
                    continue
                yield from pusher.push(queue)
                self.queues.pop(message.keyid)
