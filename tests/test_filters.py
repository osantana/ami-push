# coding: utf-8


import pytest
from panoramisk.message import Message

from filters import Filter


@pytest.fixture
def varset_message():
    return Message({"Event": "VarSet"})


@pytest.fixture
def varset_callid_message():
    return Message({"Event": "VarSet", "Variable": "CALL_ID"})


@pytest.fixture
def agentcalled_message():
    return Message({"Event": "AgentCalled"})


def test_basic_filter(varset_message, varset_callid_message, agentcalled_message):
    message_filter = Filter(event="varset")
    assert message_filter.match(varset_message)
    assert message_filter.match(varset_callid_message)
    assert not message_filter.match(agentcalled_message)


def test_compound_filter(varset_message, varset_callid_message, agentcalled_message):
    message_filter = Filter(event="varset", variable="call_id")
    assert not message_filter.match(varset_message)
    assert message_filter.match(varset_callid_message)
    assert not message_filter.match(agentcalled_message)
