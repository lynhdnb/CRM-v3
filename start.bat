@echo off
title CRM Edu Dev Launcher
chcp 65001 >nul
echo 🚀 Запуск CRM Edu (Backend + Frontend)...
echo.

:: 1. Запуск бэкенда (PowerShell)
start "CRM Backend" powershell -NoExit -Command "cd /D D:\_DEV\crm-solo\backend; .\venv\Scripts\python.exe -m uvicorn main:app --reload"

timeout /t 3 /nobreak >nul

:: 2. Запуск фронтенда (cmd — обходит политику выполнения PowerShell)
start "CRM Frontend" cmd /K "cd /D D:\_DEV\crm-solo\frontend && npm run dev"

:: 3. Информационное окно
echo.
echo ✅ Оба сервера запущены в отдельных окнах.
echo.
echo 🔹 Backend: http://127.0.0.1:8000/api/docs
echo 🔹 Frontend: http://localhost:3000
echo.
echo Нажми любую клавишу, чтобы закрыть это окно...
pause >nul
exit