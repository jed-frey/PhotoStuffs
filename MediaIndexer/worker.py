#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" ."""

import os

import get_files

import MediaIndexer.worker

from . import redis_cache, redis_utils, rq_utils


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

def cache_thumbnail(file_path, size):
    config_file = os.environ["MEDIAINDEXER_CFG"]
    databases = redis_utils.load_databases(config_file)
    cfg = {
        "file_path": file_path,
        "size": size,
        "databases": databases,
    }
    redis_cache._get_thumbnail(**cfg)

def export_thumbnail(xxhash, export_dir="/tmp", size=128):
    for key in db.keys():
        tn_ = db.get(key)
        out = os.path.join("cache", size, "{}.jpg".format(key.decode()))
        MediaIndexer.utils.pil_thumbnail(tn_).save(out)

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

    for image in get_files.get_files(directory=directory, extensions=[".jpg", ".jpeg", ".cr2", ".dng"], depth=1):
        queue.enqueue(MediaIndexer.worker.cache_exif, image)
        for size in [128, 608, 2048]:
            queue.enqueue(MediaIndexer.worker.cache_thumbnail, image, size)
