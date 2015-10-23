# coding: utf-8


import asyncio

from panoramisk import Manager


class Bridge:
    def __init__(self, **options):
        self.options = options
        self.queues = options.pop("queues", 100)
        self.max_queue_size = options.pop("max_queue_size", 100)
        self.loop = asyncio.get_event_loop()

        self.manager = Manager(loop=self.loop, **options)
        self.manager.register_event("VarSet.*", self.handle_events)

    def handle_events(self, event, manager):
        print(event, manager)

    def close(self):
        self.manager.close()
        self.loop.close()

    def run(self):
        self.manager.connect()

        try:
            self.loop.run_forever()
        finally:
            self.close()
