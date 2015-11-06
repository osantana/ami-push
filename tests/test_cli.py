# coding: utf-8


import os

import pytest

from cli import validate_config, ConfigurationError, load_config

LOCAL = os.path.dirname(__file__)


@pytest.fixture
def config_ok():
    return {
        "manager": {
            "username": "admin",
            "secret": "sekret",
        },
        "filters": {"filter": {}},
        "push": [{"url": "http://foo:bar@baz.com/", "filter": "filter"}],
    }


def test_validate_config(config_ok):
    validate_config(config_ok)


def test_invalid_config_missing_manager(config_ok):
    config_ok.pop("manager")
    with pytest.raises(ConfigurationError):
        validate_config(config_ok)


def test_invalid_config_missing_filters(config_ok):
    config_ok.pop("filters")
    with pytest.raises(ConfigurationError):
        validate_config(config_ok)


def test_invalid_config_missing_pushers(config_ok):
    config_ok.pop("push")
    with pytest.raises(ConfigurationError):
        validate_config(config_ok)


def test_invalid_config_missing_manager_username(config_ok):
    config_ok["manager"].pop("username")
    with pytest.raises(ConfigurationError):
        validate_config(config_ok)


def test_invalid_config_missing_manager_secret(config_ok):
    config_ok["manager"].pop("secret")
    with pytest.raises(ConfigurationError):
        validate_config(config_ok)


def test_invalid_config_empty_filters(config_ok):
    config_ok["filters"] = {}
    with pytest.raises(ConfigurationError):
        validate_config(config_ok)


def test_invalid_config_empty_pushers(config_ok):
    config_ok["push"] = {}
    with pytest.raises(ConfigurationError):
        validate_config(config_ok)


def test_invalid_config_invalid_filters(config_ok):
    config_ok["filters"] = ["invalid"]
    with pytest.raises(ConfigurationError):
        validate_config(config_ok)


def test_invalid_config_invalid_pushers(config_ok):
    config_ok["push"] = {"invalid"}
    with pytest.raises(ConfigurationError):
        validate_config(config_ok)


def test_load_config():
    config = load_config(os.path.join(LOCAL, "test.json"))
    assert config["manager"] == {"username": "admin", "secret": "secret"}


def test_fail_load_config():
    with pytest.raises(ConfigurationError):
        load_config("/unknown.json")
