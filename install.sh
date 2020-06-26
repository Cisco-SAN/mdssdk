#!/bin/sh
python setup.py install
unset NET_TEXTFSM
echo $(pwd)
export NET_TEXTFSM=$(pwd)/templates/
