# coding: utf-8

import os
import argparse
import configparser

import sys

from ami_push.bridge import Bridge


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", default="ami-push.cfg", metavar="FILENAME")

    arguments = parser.parse_args()

    config = configparser.ConfigParser()
    files = config.read([arguments.config, os.path.expanduser("~/.ami-push.cfg"), "/etc/ami-push.cfg"])
    file_list = ", ".join(files)

    if not config.has_section("manager"):
        parser.error("Missing [manager] section in configuration file: {}".format(file_list))
        sys.exit(1)

    options = dict(config.items("manager"))

    if "username" not in options:
        parser.error("Missing username in {}".format(", ".join(files)))
        sys.exit(1)

    if "secret" not in options:
        parser.error("Missing secret in {}".format(", ".join(files)))
        sys.exit(1)

    # remove unused and invalid options
    options.pop("loop", None)
    options.pop("events", None)
    options.pop("connection_class", None)

    bridge = Bridge(**options)
    bridge.run()


if __name__ == "__main__":
    main()
