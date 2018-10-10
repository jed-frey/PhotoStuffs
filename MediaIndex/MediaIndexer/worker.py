#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""."""

from . import redis_utils
from . import redis_cache
from . import rq_utils
import MediaIndexer.worker
import os

def cache_xxhash(file_path):
    config_file = os.environ["MEDIAINDEXER_CFG"]
    databases = redis_utils.load_databases(config_file)
    cfg = {
        "file_path": file_path,
        "databases": databases,
    }
    redis_cache._get_xxhash(**cfg)

def cache_exif(file_path):
    config_file = os.environ["MEDIAINDEXER_CFG"]
    databases = redis_utils.load_databases(config_file)
    cfg = {
        "file_path": file_path,
        "databases": databases,
    }
    redis_cache._get_exif(**cfg)
import get_files
def cache_thumbnail(file_path):
    config_file = os.environ["MEDIAINDEXER_CFG"]
    databases = redis_utils.load_databases(config_file)
    cfg = {
        "file_path": file_path,
        "databases": databases,
    }
    redis_cache._get_thumbnail(**cfg)

def scan_dir(directory):
    """Scan a directory.

    1. Queue a scan of any found directories.
    2. Queue exif & thumbnail caching for any .jpeg files found.
    """
    config_file = os.environ.get("MEDIAINDEXER_CFG", "config.ini")
    queue = rq_utils.get_queue(config_file=config_file, database="rq")

    for d in get_files.get_dirs(directory=directory, depth=1):
        if d.startswith("."):
            continue
        if ".zfs" in d:
            continue
        queue.enqueue(MediaIndexer.worker.scan_dir, d)

    for image in get_files.get_files(directory=directory, extensions=[".jpg", ".jpeg"], depth=1):
        queue.enqueue(MediaIndexer.worker.cache_exif, image)
        queue.enqueue(MediaIndexer.worker.cache_thumbnail, image)
