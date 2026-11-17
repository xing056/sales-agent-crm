@echo off
chcp 65001 >nul
title 前端 Vue :5173
cd /d "%~dp0..\frontend"

if not exist "node_modules" (
  echo [提示] 首次运行需要安装依赖，大约 1-3 分钟
  call npm install
)

call npm run dev
pause
