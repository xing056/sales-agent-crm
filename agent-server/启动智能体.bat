@echo off
chcp 65001 >nul
title CRM 智能体启动器
cd /d "%~dp0"

echo ================================================
echo   1. 启动 Django 后端（端口 8000）
echo   2. 启动 CRM 智能体（端口 8200）
echo ================================================
echo.

if not exist "..\backend\manage.py" (
  echo [错误] 找不到 ..\backend\manage.py
  echo        请从仓库根目录运行 启动演示.bat
  pause & exit /b 1
)

set BACK_PY=python
if exist "..\backend\.venv\Scripts\python.exe" set BACK_PY=..\backend\.venv\Scripts\python.exe

start "后端 Django :8000" cmd /k "cd /d %~dp0..\backend && %BACK_PY% manage.py runserver 8000"
timeout /t 6 >nul

set AGENT_PY=python
if exist ".venv\Scripts\python.exe" set AGENT_PY=.venv\Scripts\python.exe

start "CRM 智能体 :8200" cmd /k "cd /d %~dp0 && %AGENT_PY% server.py"
timeout /t 4 >nul

start "" http://127.0.0.1:8200/
echo 已打开 http://127.0.0.1:8200/
echo 关闭这个窗口不会停止服务，服务在各自的黑窗口里。
pause
