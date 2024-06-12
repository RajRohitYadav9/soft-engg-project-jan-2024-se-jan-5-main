@echo off

:: Check if virtual environment exists
if not exist .venv (
    echo Creating virtual environment...
    python -m venv .venv
)

:: Activate virtual environment
.venv\Scripts\activate

:: Notify the user
echo.
echo Virtual environment is activated. Type 'deactivate' to exit the virtual environment.
echo.
