# Start AutoMate Full Stack
# This script starts both the API server and the web UI

Write-Host "🚀 Starting AutoMate Full Stack..." -ForegroundColor Cyan
Write-Host ""

# Function to start API in a new window
function Start-API {
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "& '.\start_api.ps1'"
}

# Function to start Web UI in a new window
function Start-Web {
    $webScript = @"
Write-Host '🌐 Starting AutoMate Web UI...' -ForegroundColor Cyan
Write-Host ''
cd web
npm run dev
"@
    Start-Process powershell -ArgumentList "-NoExit", "-Command", $webScript
}

Write-Host "🔧 Launching API Server..." -ForegroundColor Yellow
Start-API
Start-Sleep -Seconds 2

Write-Host "🌐 Launching Web UI..." -ForegroundColor Yellow
Start-Web

Write-Host ""
Write-Host "✅ Both servers are starting!" -ForegroundColor Green
Write-Host ""
Write-Host "📡 API Server: http://localhost:8000" -ForegroundColor Cyan
Write-Host "🌐 Web UI: http://localhost:3000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Check the new terminal windows for server logs." -ForegroundColor Yellow
Write-Host "Press any key to exit this launcher..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')
