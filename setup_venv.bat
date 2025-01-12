@echo off

:: Create the virtual environment
python -m venv .venv

:: Activate the virtual environment
call .venv\Scripts\activate.bat

:: Install dependencies if requirements.txt exists
pip install -r requirements.txt

pause