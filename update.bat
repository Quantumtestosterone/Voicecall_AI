@echo off

REM Activate the virtual environment
call venv\Scripts\activate

REM Upgrade pip
python -m pip install --upgrade pip

REM Upgrade required packages
pip install --upgrade streamlit anthropic groq python-dotenv aiohttp twilio deepgram-sdk

REM Deactivate the virtual environment
deactivate

echo Libraries have been updated.
pause