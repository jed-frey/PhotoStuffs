#!/usr/bin/env python3
"""."""
import uuid

import rq

import MediaIndexer
from .redis_utils import load_databases
from MediaIndexer import redis_cache


def get_connection(config_file, database):
    databases = load_databases(config_file)
    return databases[database]


def get_queue(**kwargs):
    connection = get_connection(**kwargs)
    return rq.Queue(connection=connection)


def get_worker(**kwargs):
    connection = get_connection(**kwargs)
    return rq.Worker("default", connection=connection)
