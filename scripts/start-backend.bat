@echo off
chcp 65001 >nul
title 后端 Django :8000
cd /d "%~dp0..\backend"

if exist ".venv\Scripts\python.exe" (
  set PY=.venv\Scripts\python.exe
) else (
  set PY=python
)

echo [后端] 使用解释器：%PY%
%PY% manage.py runserver 8000
pause
