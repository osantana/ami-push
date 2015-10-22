# coding: utf-8

import os
import argparse
import configparser


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", default="ami-push.cfg", metavar="FILENAME")

    arguments = parser.parse_args()

    config = configparser.ConfigParser()
    config.read([arguments.config, os.path.expanduser("~/.ami-push.cfg"), "/etc/ami-push.cfg"])

    print(config.sections())


if __name__ == "__main__":
    main()
