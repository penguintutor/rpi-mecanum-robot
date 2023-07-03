#!/bin/bash
# 10s delay to give desktop chance to fully start
sleep 10s
antimicrox --tray &
/opt/mecanum/mecanum.py
