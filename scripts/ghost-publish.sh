#!/bin/bash
# Wrapper script for the python publisher
PYTHON_SCRIPT="$(dirname "$0")/ghost-publish.py"
python3 "$PYTHON_SCRIPT" "$@"
