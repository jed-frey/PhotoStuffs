#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""."""
import configparser
import os
import sys

import redis
from .config import read_config

def load_databases(config):
    """."""

    if isinstance(config, configparser.ConfigParser):
        config = config
    if config is None:
        config = read_config(config_file=config_file)
    databases = dict()
    for key in config["redis"].keys():
        if key in ["host", "port"]:
            continue
        db_ = redis.StrictRedis(
            host=config["redis"]["host"],
            port=config["redis"]["port"],
            db=config["redis"][key],
        )
        databases[key] = db_
    return databases


