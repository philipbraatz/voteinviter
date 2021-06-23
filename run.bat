@echo off
title Vote Inviter

pip install -r requirements.txt

python app.py web
python app.py bot

pause