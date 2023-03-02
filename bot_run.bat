@echo off

call %~dp0telegram_bot\venv\Scripts\activate

cd %~dp0telegram_bot

set TOKEN = YOUR BOT TOKEN

python bot_telegram.py

pause
