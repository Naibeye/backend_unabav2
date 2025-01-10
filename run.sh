#!/bin/bash
dvenv="venv"
[ ! -d "$dvenv" ] && python3 -m venv venv || echo "OK"
kill $(lsof -ti :$1)
source venv/bin/activate || exit
pip install -r requirements.txt || exit
gunicorn -w 8 -b 0.0.0.0:$1 'app:app'  > /dev/null 2>&1 &
