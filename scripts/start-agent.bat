@echo off
chcp 65001 >nul
title CRM 智能体 :8200
cd /d "%~dp0..\agent-server"

if exist ".venv\Scripts\python.exe" (
  set PY=.venv\Scripts\python.exe
) else (
  set PY=python
)

if not exist ".env" (
  echo [提示] 未找到 agent-server\.env
  echo        请把 .env.example 复制为 .env，并填写 LLM_API_KEY
  echo.
)

echo [智能体] 使用解释器：%PY%
%PY% server.py
pause
