# coding: utf-8


import asyncio
import logging

from panoramisk import Manager


logger = logging.getLogger(__name__)


class Bridge:
    def __init__(self, **options):
        self.options = options
        self.queues = options.pop("queues", 100)
        self.max_queue_size = options.pop("max_queue_size", 100)
        self.loop = asyncio.get_event_loop()

        self.manager = Manager(loop=self.loop, **options)
        self.manager.register_event("*", self.handle_events)

    def handle_events(self, manager, event):
        print(event)

    def run(self):
        self.manager.connect()

        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            logger.info("Interrupted... Exiting!")
        finally:
            self.loop.close()
