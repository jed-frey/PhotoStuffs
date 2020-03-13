#!/bin/sh

isort --apply --settings-path ../setup.cfg *.py
black --target-version py37 --line-length 79 *.py
git add *.py
git commit -m "isorted and blackened python files"
