@echo off
title THE REMYVERSE PUBLISHER - V4.0 (The Newsroom)
color 0E

echo.
echo ==================================================
echo      PHASE 1: SCOUTING (Intel Gathering)
echo ==================================================
echo.
:: Run the scout from its folder
cd Assets
python scout.py
cd ..

if %errorlevel% neq 0 (
    echo.
    echo ❌ SCOUT FAILED. Continuing with cached intel...
)

echo.
echo ==================================================
echo      PHASE 2: NIGHT SHIFT (The Generators)
echo ==================================================
echo.
:: Run the new Modular Newsroom
:: Ensure you are in the project root
python -m newsroom.main

if %errorlevel% neq 0 (
    echo.
    echo ❌ NEWSROOM CRASHED. CHECK PYTHON ERROR ABOVE.
    pause
    exit /b
)

echo.
echo ==================================================
echo      PHASE 3: DEPLOYMENT (Push to Web)
echo ==================================================
echo.
:: Move to the Next.js app folder
cd fairground
git add .
git commit -m "Fresh Issue: 4-Pillar Layout"
git push

echo.
echo ==================================================
echo      SUCCESS! CHECK THEREMYVERSE.COM
echo ==================================================
echo.
pause