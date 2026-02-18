# ============================================================================
# Löneprocess API - Run both v1 and v2 in parallel
# ============================================================================

# Configuration
$API_V1_PORT = 8000
$API_V2_PORT = 8001
$PROJECT_PATH = Split-Path -Parent $MyInvocation.MyCommand.Path
$API_PATH = Join-Path $PROJECT_PATH "loneprocess-api"

Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "🚀 Löneprocess API - Startar båda versioner" -ForegroundColor Green
Write-Host "============================================================================" -ForegroundColor Cyan

# Check if already running
Write-Host "`n📋 Kontrollerar om portarna är lediga..." -ForegroundColor Yellow

$process_v1 = Get-NetTCPConnection -LocalPort $API_V1_PORT -ErrorAction SilentlyContinue
$process_v2 = Get-NetTCPConnection -LocalPort $API_V2_PORT -ErrorAction SilentlyContinue

if ($process_v1) {
    Write-Host "⚠️  Port $API_V1_PORT är redan i användning. Stänger gammal process..." -ForegroundColor Yellow
    Stop-Process -Port $API_V1_PORT -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 1
}

if ($process_v2) {
    Write-Host "⚠️  Port $API_V2_PORT är redan i användning. Stänger gammal process..." -ForegroundColor Yellow
    Stop-Process -Port $API_V2_PORT -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 1
}

Write-Host "`n✨ Startar API v1 på port $API_V1_PORT..." -ForegroundColor Green
Write-Host "   Kommando: python standalone_api.py" -ForegroundColor Gray

# Start v1 in background
Push-Location $API_PATH
$process_v1_id = (Start-Process -FilePath python -ArgumentList "standalone_api.py" -NoNewWindow -PassThru).Id
Write-Host "   ✓ Started (PID: $process_v1_id)" -ForegroundColor Green

Start-Sleep -Seconds 3

Write-Host "`n✨ Startar API v2 på port $API_V2_PORT..." -ForegroundColor Green
Write-Host "   Kommando: python standalone_api_v2.py --port 8001" -ForegroundColor Gray

# Start v2 in background with different port
$process_v2_id = (Start-Process -FilePath python -ArgumentList "standalone_api_v2.py" -NoNewWindow -PassThru).Id
Write-Host "   ✓ Started (PID: $process_v2_id)" -ForegroundColor Green

Pop-Location

Write-Host "`n============================================================================" -ForegroundColor Cyan
Write-Host "✅ Båda API:er är nu igång!" -ForegroundColor Green
Write-Host "============================================================================" -ForegroundColor Cyan

Write-Host "`n📊 API Status:" -ForegroundColor Yellow
Write-Host "   v1 Swagger UI:     http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "   v1 ReDoc:          http://localhost:8000/redoc" -ForegroundColor Cyan
Write-Host "   v1 Health:         http://localhost:8000/health" -ForegroundColor Cyan

Write-Host ""
Write-Host "   v2 Swagger UI:     http://localhost:8001/docs" -ForegroundColor Cyan
Write-Host "   v2 ReDoc:          http://localhost:8001/redoc" -ForegroundColor Cyan
Write-Host "   v2 Health:         http://localhost:8001/health" -ForegroundColor Cyan

Write-Host "`n📝 Process IDs:" -ForegroundColor Yellow
Write-Host "   v1: $process_v1_id" -ForegroundColor Gray
Write-Host "   v2: $process_v2_id" -ForegroundColor Gray

Write-Host "`n🛑 Använd följande för att stoppa:" -ForegroundColor Yellow
Write-Host "   Stop-Process -Id $process_v1_id -Force  # Stoppa v1" -ForegroundColor Gray
Write-Host "   Stop-Process -Id $process_v2_id -Force  # Stoppa v2" -ForegroundColor Gray
Write-Host "   atau ketik Ctrl+C för att stoppa båda" -ForegroundColor Gray

Write-Host "`n============================================================================`n" -ForegroundColor Cyan

# Keep the script running and show status
Write-Host "🔍 Övervakar processer..." -ForegroundColor Yellow
while ($true) {
    $v1_running = Get-Process -Id $process_v1_id -ErrorAction SilentlyContinue
    $v2_running = Get-Process -Id $process_v2_id -ErrorAction SilentlyContinue
    
    if (-not $v1_running) {
        Write-Host "❌ API v1 har stannat!" -ForegroundColor Red
        break
    }
    
    if (-not $v2_running) {
        Write-Host "❌ API v2 har stannat!" -ForegroundColor Red
        break
    }
    
    Start-Sleep -Seconds 5
}

Write-Host "`nExit.`n" -ForegroundColor Yellow
