#!/bin/bash

# cd too current directory
cd $(dirname $0)
/usr/bin/python3 week_playlist.py

find . -type d -name 'Week*' -exec tar -cvfz {}.tar.gz {} \;
find . -type d -name 'Week*' -exec rm -rf {} \;
echo "#########################"
echo "### Empty file in tar ###"
echo "#########################"
find . -type f -name 'Week_*' -mtime 0 -exec tar -vtf {} \; | awk '{if ($3 =="0") print $3,$5,$6}' | grep -v '\/$'