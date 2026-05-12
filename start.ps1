# Принудительная UTF-8 для корректного вывода эмодзи и кириллицы
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host " Запуск CRM Edu (Backend + Frontend)..." -ForegroundColor Cyan
Write-Host ""

# --- BACKEND ---
# Команда обернута в try/catch + Read-Host. Окно НЕ закроется при ошибке.
$backendCmd = "Set-Location 'D:\_DEV\crm-solo\backend'; Write-Host '📦 Запуск uvicorn...' -ForegroundColor Yellow; try { & '.\venv\Scripts\python.exe' -m uvicorn main:app --reload } catch { Write-Host '❌ Ошибка Backend: ' + $_.Exception.Message -ForegroundColor Red }; Read-Host 'Backend окно закрыто. Нажмите Enter...'"
Start-Process powershell.exe -ArgumentList "-NoExit", "-Command", $backendCmd -WindowStyle Normal

Start-Sleep -Seconds 2

# --- FRONTEND ---
# Флаг /K в CMD оставляет окно открытым даже после завершения/ошибки npm
$frontendCmd = "cd /D D:\_DEV\crm-solo\frontend && npm run dev"
Start-Process cmd.exe -ArgumentList "/K", $frontendCmd -WindowStyle Normal

# --- ГЛАВНОЕ ОКНО ---
Write-Host "✅ Серверы запущены в отдельных окнах!" -ForegroundColor Green
Write-Host "🔹 Backend Docs: http://127.0.0.1:8000/api/docs"
Write-Host " Frontend App:  http://localhost:3000"
Write-Host ""
Write-Host "⚠️ Если какое-то окно мигает и закрывается — оно откроется снова, но останется висеть с ошибкой." -ForegroundColor Yellow
Read-Host "Нажмите Enter, чтобы закрыть это главное окно (серверы продолжат работать)"