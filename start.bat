@echo off
echo Starting Ticino Real Estate Bot...
echo.

if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing/updating dependencies...
pip install -r requirements.txt
echo.

echo Starting bot...
python main.py

pause
