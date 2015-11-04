# coding: utf-8


from handlers import Handler


def test_basic_handler():
    handler = Handler(filter="varset-callid", action="enqueue")
    assert handler.action == "enqueue"
    assert handler.filter == "varset-callid"
