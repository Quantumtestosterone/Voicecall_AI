@echo off

REM Activate the virtual environment
call venv\Scripts\activate

REM Upgrade pip
python -m pip install --upgrade pip

REM Upgrade required packages
pip install requirements.txt

REM Deactivate the virtual environment
deactivate

echo Libraries have been updated.
pause