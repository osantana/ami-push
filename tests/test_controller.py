# coding: utf-8


import asyncio

from controller import Controller, DEFAULT_MAX_QUEUE_SIZE


def test_basic_controller():
    controller = Controller()
    assert controller.loop == asyncio.get_event_loop()
    assert controller.max_queue_size == DEFAULT_MAX_QUEUE_SIZE
    assert len(controller.queues) == 0


def test_controller_config():
    controller = Controller()
    controller.load_configs(
        filters={"test-filter": {"event": "NoOp"}},
        handlers=[{"action": "enqueue", "filter": "test-filter"}],
    )
    assert controller.filters["test-filter"].rules == {"event": "NoOp"}
    assert controller.handlers[0].action == "enqueue"
    assert controller.handlers[0].filter == "test-filter"
