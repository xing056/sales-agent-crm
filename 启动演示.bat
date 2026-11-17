@echo off
chcp 65001 >nul
title sales-agent-crm 一键启动
cd /d "%~dp0"

echo ==========================================================
echo   sales-agent-crm 演示环境
echo     1. Django 后端     http://127.0.0.1:8000
echo     2. CRM 智能体      http://127.0.0.1:8200
echo     3. Vue 后台管理    http://127.0.0.1:5173
echo ==========================================================
echo.

start "后端 Django :8000" cmd /k "%~dp0scripts\start-backend.bat"
timeout /t 8 >nul

start "CRM 智能体 :8200" cmd /k "%~dp0scripts\start-agent.bat"
timeout /t 3 >nul

start "前端 Vue :5173" cmd /k "%~dp0scripts\start-frontend.bat"
timeout /t 12 >nul

start "" http://127.0.0.1:5173/
echo 已打开后台管理页面。登录后点右下角悬浮球即可唤起智能体。
echo 三个服务在各自的窗口里运行，关掉本窗口不会停止它们。
pause
