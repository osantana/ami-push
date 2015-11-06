# coding: utf-8


from pusher import Pusher


def test_basic_pusher():
    pusher = Pusher(filter="varset-callid", url="http://foo:bar@baz.com")
    assert pusher.filter == "varset-callid"
    assert pusher.url == "http://foo:bar@baz.com"
