# coding: utf-8

import os
import argparse
import json

import sys

from ami_push.bridge import Bridge


def _load_config(filename):
    filenames = ("/etc/ami-push.json", os.path.expanduser("~/.ami-push.json"), filename)
    for filename in filenames:
        try:
            with open(filename) as file_:
                return json.load(file_)
        except OSError:
            continue
    else:
        raise OSError("Cannot open configuration files: {}".format(", ".join(filenames)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", default="ami-push.json", metavar="FILENAME")
    arguments = parser.parse_args()

    try:
        config = _load_config(arguments.config)
    except OSError as ex:
        parser.error(str(ex))
        sys.exit(1)

    if "manager" not in config:
        parser.error('Missing "manager" section in configuration.')
        sys.exit(1)

    if "username" not in config["manager"]:
        parser.error("Missing username configuration")
        sys.exit(1)

    if "secret" not in config["manager"]:
        parser.error("Missing secret configuration")
        sys.exit(1)

    bridge = Bridge(config["manager"], config["rules"])

    try:
        bridge.run()
    except OSError as ex:
        parser.error(str(ex))
        sys.exit(2)


if __name__ == "__main__":
    main()
