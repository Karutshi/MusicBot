#!/bin/bash

if [[ $(whoami) != "root" ]]; then
    echo "Please run as root!"
    exit 1
fi

kill $(cat pid.txt)
rm pid.txt
