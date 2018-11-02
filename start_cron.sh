#!/bin/bash

# cd too current directory
cd $(dirname $0)
/usr/bin/python3 week_playlist.py

find . -type d -name 'Week*' -exec tar -cvf {}.tar {} \;
find . -type d -name 'Week*' -exec rm -rf {} \;
echo "##########################"
echo "########## tar ###########"
echo "##########################"
find . -type f -name 'Week_*' -mtime 0 -exec tar -vtf {} \; | sort -n | grep -v '\/$' | awk '{print $3,$5,$6}'
