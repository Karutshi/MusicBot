#!/bin/bash

if [[ $(whoami) != "root" ]]; then
    echo "Please run as root!"
    exit 1
fi

python3.5 -V > /dev/null 2>&1 || {
	echo >&2 "Python 3.5 doesn't seem to be installed.  Do you have a weird installation?"
	echo >&2 "If you have python 3.5, use it to run run.py instead of this script."
	exit 1; }

rm -f nohup.out
su johan -c "touch nohup.out"
nohup python3.5 run.py & 
echo "$!" > pid.txt
