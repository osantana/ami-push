# coding: utf-8


import json

from panoramisk import utils
from panoramisk.message import Message

from messages import MessageWrapper


MESSAGE = """
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
Context: income-call
Exten: test
Priority: 4
Uniqueid: 1444884710.0
Variable: CALL_ID
Value: 5aeb879d-753e-48f2-92da-22ae0653cee8
""".replace("\n", utils.EOL)


def test_message_from_message():
    message = Message({"Uniqueid": "1444884710.0"})
    wrapper = MessageWrapper(message)
    assert wrapper.uniqueid == "1444884710.0"
    assert wrapper.keyid == "1444884710"


def test_message_from_text():
    wrapper = MessageWrapper(MESSAGE)
    assert wrapper.uniqueid == "1444884710.0"

    assert "language" in wrapper
    assert wrapper.language == "en"
    assert wrapper["language"] == "en"

    assert "variable" in wrapper
    assert wrapper.variable == "CALL_ID"
    assert wrapper["variable"] == "CALL_ID"

    assert "value" in wrapper
    assert wrapper.value == "5aeb879d-753e-48f2-92da-22ae0653cee8"
    assert wrapper["value"] == "5aeb879d-753e-48f2-92da-22ae0653cee8"


def test_message_to_json():
    wrapper = MessageWrapper(MESSAGE)
    decoded = json.loads(wrapper.json())

    assert decoded["Uniqueid"] == "1444884710.0"
    assert decoded["Language"] == "en"
    assert decoded["Variable"] == "CALL_ID"
    assert decoded["Value"] == "5aeb879d-753e-48f2-92da-22ae0653cee8"
