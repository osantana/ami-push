# coding: utf-8

from unittest.mock import Mock

import pytest
from panoramisk import utils
from panoramisk.message import Message

from ami_push.bridge import Controller

EVENT = """
Event: VarSet
Privilege: dialplan,all
Channel: SIP/test
ChannelState: 4
ChannelStateDesc: Ring
CallerIDNum: 0055551234
CallerIDName: 0055551234
ConnectedLineNum: <unknown>
ConnectedLineName: <unknown>
Language: en
AccountCode:
Context: income-call
Exten: test
Priority: 4
Uniqueid: 1444884710.0
Variable: CALL_ID
Value: 5aeb879d-753e-48f2-92da-22ae0653cee8
"""


@pytest.yield_fixture
def event_message():
    def _message(data):
        return Message.from_line(data)

    eol = utils.EOL
    utils.EOL = '\n'
    yield _message
    utils.EOL = eol


def test_basic_controller():
    controller = Controller()
    assert controller.loop is not None


def test_controller_custom_loop():
    loop = Mock()
    controller = Controller(loop=loop)
    assert controller.loop == loop

# def test_basic_handler(event_message):
#     message = event_message(EVENT)
#     controller = Mock(spec_set=Controller)
#     handler = Handler(event="varset", action="append", filters={"variable": "call_id"})
#     handler.handle(controller, message)
#
#
# def test_basic_rule():
#     rule = Rule("test-rule", handlers=[])
#     assert rule.name == "test-rule"
