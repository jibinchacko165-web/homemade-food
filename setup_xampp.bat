@echo off
REM Automated Setup Script for XAMPP MySQL Integration
REM This script sets up the Django project with XAMPP MySQL

echo.
echo ========================================
echo Homemade Food Order System - XAMPP Setup
echo ========================================
echo.

REM Check if virtual environment exists
if not exist venv (
    echo ERROR: Virtual environment not found!
    echo Please create it first with: python -m venv venv
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

echo.
echo [1/5] Checking Django installation...
python manage.py --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Django not found. Installing dependencies...
    pip install -r requirements.txt
) else (
    echo OK: Django found
)

echo.
echo [2/5] Checking MySQL connection...
python manage.py dbshell <nul >nul 2>&1
if errorlevel 1 (
    echo WARNING: Cannot connect to MySQL
    echo Make sure XAMPP MySQL is running!
    echo.
    echo Instructions:
    echo 1. Open XAMPP Control Panel
    echo 2. Click "Start" next to MySQL
    echo 3. Wait a few seconds and run this script again
    echo.
    pause
    exit /b 1
) else (
    echo OK: MySQL connection successful
)

echo.
echo [3/5] Running database migrations...
python manage.py migrate
if errorlevel 1 (
    echo ERROR: Migration failed
    pause
    exit /b 1
) else (
    echo OK: Migrations completed
)

echo.
echo [4/5] Loading sample data...
python add_malayalam_foods.py
if errorlevel 1 (
    echo WARNING: Could not load Malayalam foods
)

echo.
echo [5/5] Setup complete!
echo.
echo ========================================
echo Next Steps:
echo ========================================
echo 1. To create an admin account, run:
echo    python manage.py createsuperuser
echo.
echo 2. To start the development server:
echo    python manage.py runserver
echo.
echo 3. Visit: http://localhost:8000
echo.
echo ========================================
echo.
pause
