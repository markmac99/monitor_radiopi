#!/bin/bash
#
# script to check and restart allsky if frozen
# Copyright (C) Mark McIntyre
#

srcdir="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

cd $srcdir
source $HOME/miniconda3/bin/activate ukmon-shared

BROKER=broker
MQUSER=mquser
MQPASS=mqpass

lastupdate=$(mosquitto_sub -h ${BROKER} -u ${MQUSER} -P ${MQPASS} -t meteorcams/radiopi/timestamp -i checkradio -C 1 -W 20)
[ "$lastupdate" == "" ] && lastupdate="2026-01-01T00:00:00Z"
python -c "from sendRadioAlert import checkAndSend;checkAndSend('$lastupdate');"
