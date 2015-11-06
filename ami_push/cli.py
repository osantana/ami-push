# coding: utf-8

import argparse
import json
import os
import sys

from ami_push.bridge import Bridge


class ConfigurationError(Exception):
    pass


def load_config(filename):
    config = None
    filenames = (filename, "/etc/ami-push.json", os.path.expanduser("~/.ami-push.json"))
    for filename in filenames:
        try:
            with open(filename) as file_:
                config = json.load(file_)
        except OSError:
            continue

    if config is None:
        raise ConfigurationError("Cannot open configuration files: {}".format(", ".join(filenames)))

    return validate_config(config)


def validate_config(config):
    if "manager" not in config:
        raise ConfigurationError('Missing "manager" section in configuration.')

    if "username" not in config["manager"]:
        raise ConfigurationError("Missing username configuration")

    if "secret" not in config["manager"]:
        raise ConfigurationError("Missing secret configuration")

    if "filters" not in config:
        raise ConfigurationError('Missing "filters" section in configuration.')

    if not config["filters"]:
        raise ConfigurationError('No filter specified.')

    if not isinstance(config["filters"], dict):
        raise ConfigurationError("Invalid filters specification.")

    if "push" not in config:
        raise ConfigurationError('Missing "push" section in configuration.')

    if not config["push"]:
        raise ConfigurationError('No push configuration specified.')

    if not isinstance(config["push"], list):
        raise ConfigurationError("Push configurations must be in a list.")

    return config


def main(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", default="ami-push.json", metavar="FILENAME")
    arguments = parser.parse_args(args)

    try:
        config = load_config(arguments.config)
    except ConfigurationError as ex:
        parser.error(str(ex))
        return 1

    bridge = Bridge(config["manager"], config["filters"], config["push"])

    try:
        bridge.run()
    except OSError as ex:
        parser.error(str(ex))
        return 2


if __name__ == "__main__":
    sys.exit(int(main()))
