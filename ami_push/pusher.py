# coding: utf-8


import json
import asyncio

import aiohttp


# noinspection PyShadowingBuiltins
class Pusher:
    def __init__(self, filter, url):
        self.filter = filter
        self.url = url

    def push(self, queue):
        messages = []
        while True:
            try:
                message = queue.get_nowait()
            except asyncio.QueueEmpty:
                break
            messages.append(message.json())

        headers = {'content-type': 'application/json'}
        payload = json.dumps(messages)
        response = yield from aiohttp.post(self.url, data=payload, headers=headers)
        return (yield from response.read())
