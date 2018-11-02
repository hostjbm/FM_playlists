#!/bin/bash

# cd too current directory
cd $(dirname $0)
/usr/bin/python3 week_playlist.py

find . -type d -name 'Week*' -exec tar -cvf {}.tar {} \;
find . -type d -name 'Week*' -exec rm -rf {} \;
