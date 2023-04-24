#!/bin/bash

#PATH_TO_IP_BLOCKER="W tej zmiennej wpisujemy ścieżkę do naszego folderu z konfiguracją i skryptem"
PATH_TO_IP_BLOCKER=/opt/ip_blocker/

cd $PATH_TO_IP_BLOCKER
python3 ip_blocker.py
