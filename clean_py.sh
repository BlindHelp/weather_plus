#!/bin/sh
# recursively removes all .pyc , .pyo files and __pycache__ directories in the current
# directory
find . | \
  grep -E "(__pycache__|\.pyc$|\.pyo$)" | \
  xargs rm -rf
