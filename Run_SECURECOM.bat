@echo off
title SECURECOM Advanced
cd /d "%~dp0"
set "PYTHON=C:\Users\ZIA COMPUTERS\.conda\envs\phishingdetector\python.exe"
if exist "%PYTHON%" (
  "%PYTHON%" -m pip show cryptography >nul 2>&1
  if errorlevel 1 (
    echo Installing required package...
    "%PYTHON%" -m pip install -r requirements.txt
  )
  "%PYTHON%" app.py
  if errorlevel 1 pause
) else (
  py -m pip install -r requirements.txt
  py app.py
  if errorlevel 1 pause
)
