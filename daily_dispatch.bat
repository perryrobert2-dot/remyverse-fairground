@echo off
title THE REMY DIGEST - CONTROL ROOM
color 0e

echo.
echo ========================================================
echo  PHASE 1: THE SCOUT
echo  Fetching local news and political receipts...
echo ========================================================
python scout.py

echo.
echo.
echo ========================================================
echo  PHASE 2: THE RUPERT INTERVENTION (EDITORIAL OVERRIDE)
echo ========================================================
echo.
echo  [STOP] The system has gathered the raw data.
echo.
echo  [AUTO] Running The Darkroom (Converting PNGs to JPGs)...
python convert_art.py
echo.
echo  [ACTION REQUIRED]:
echo   1. Check 'wire_copy.json' (The News)
echo   2. Check 'fight_card.json' (The PITD Matchup)
echo   3. Check 'saga.json' (The Arthur Pumble Story)
echo   4. Ensure your images (pitd_current.jpg, etc) are in content/images/
echo.
echo  Edit any files you wish, save them, and then...
echo.
echo  Press any key when you are ready to start the Presses...
pause >nul

echo.
echo ========================================================
echo  PHASE 3: THE NEWSROOM (ASSEMBLE)
echo  The Staff are writing their columns...
echo ========================================================
python assemble.py

echo.
echo ========================================================
echo  PHASE 4: THE PUBLISHER
echo  Merging content into the Broadsheet Layout...
echo ========================================================
python publish.py

echo.
echo ========================================================
echo  PHASE 5: DISTRIBUTION (CLOUD DEPLOY)
echo  Sending the edition to the printing press (GitHub/Vercel)...
echo ========================================================
git add .
git commit -m "Daily Dispatch: Auto-publish via Control Room"
git push

echo.
echo ========================================================
echo  [SUCCESS] EDITION PUBLISHED.
echo  Check your phone in 60 seconds.
echo ========================================================
pause