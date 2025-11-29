#!/bin/bash

source myenv/bin/activate
nohup python3 Funt_2.0.py > log.txt 2>&1 &
echo "✅ Бот запущен"
