#! /bin/sh
PIDNum=$(ps aux | grep "python" | grep "piSerPrint.py" | grep -v "grep" | grep -v "sudo" | sed 's@^[^0-9]*\([0-9]\+\).*@\1@')
ps aux
echo "${PIDNum}"
sudo kill "${PIDNum}"
sudo minicom
