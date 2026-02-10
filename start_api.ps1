# Start AutoMate API Server
# Run this from the main autoMate directory

Write-Host "🚀 Starting AutoMate API Server..." -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (!(Test-Path ".venv\Scripts\activate.ps1")) {
    Write-Host "❌ Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run 'uv sync' first to create the environment." -ForegroundColor Yellow
    exit 1
}

# Activate virtual environment
Write-Host "📦 Activating virtual environment..." -ForegroundColor Yellow
& .\.venv\Scripts\activate.ps1

# Check if FastAPI is installed
Write-Host "🔍 Checking dependencies..." -ForegroundColor Yellow
python -c "import fastapi, uvicorn" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ FastAPI not installed!" -ForegroundColor Red
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    uv pip install fastapi uvicorn[standard] python-multipart
}

Write-Host ""
Write-Host "✅ Ready to start!" -ForegroundColor Green
Write-Host ""
Write-Host "📡 API Server: http://localhost:8000" -ForegroundColor Cyan
Write-Host "📖 API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start the API server with uv run to ensure correct environment
uv run python api_server.py
