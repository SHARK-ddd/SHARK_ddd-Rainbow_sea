<#
.SYNOPSIS
SmartLab AIoT - One-click Start Script
智慧实验室监测系统一键启动脚本

.DESCRIPTION
This script starts all required services for the SmartLab AIoT system:
1. MQTT Broker (if available)
2. Backend API Server
3. Frontend Dashboard
#>

$ErrorActionPreference = "Stop"

# Check if Python is available
try {
    python --version | Out-Null
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if in correct directory
if (-not (Test-Path "backend/main.py")) {
    Write-Host "ERROR: Please run this script from the SmartLab-AIoT directory" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "    SmartLab AIoT Monitoring System" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Start MQTT Broker if Mosquitto is available
$mosquittoPath = "D:\Mosquitto\mosquitto.exe"
if (Test-Path $mosquittoPath) {
    Write-Host "[1/3] Starting MQTT Broker..." -ForegroundColor Green
    $mqttDir = "D:\Mosquitto"
    $mqttConfig = "$mqttDir\mosquitto_custom.conf"
    
    $configContent = @"
listener 1883
allow_anonymous true
"@
    
    [System.IO.File]::WriteAllText($mqttConfig, $configContent)
    Start-Process -FilePath $mosquittoPath -ArgumentList "-c `"$mqttConfig`"" -WindowStyle Minimized
    Start-Sleep -Seconds 2
} else {
    Write-Host "[1/3] MQTT Broker not found at $mosquittoPath" -ForegroundColor Yellow
    Write-Host "      Continuing without MQTT..." -ForegroundColor Yellow
}

# Start Backend Server
Write-Host "[2/3] Starting Backend Server..." -ForegroundColor Green
Start-Process -FilePath "python" -ArgumentList "main.py" -WorkingDirectory "backend" -WindowStyle Minimized
Start-Sleep -Seconds 3

# Start Frontend Server
Write-Host "[3/3] Starting Frontend Server..." -ForegroundColor Green
Start-Process -FilePath "python" -ArgumentList "-m http.server 8080" -WorkingDirectory "frontend" -WindowStyle Minimized
Start-Sleep -Seconds 2

# Open Frontend in default browser
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "          System Started Successfully!" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Backend API:    http://localhost:8000" -ForegroundColor White
Write-Host "Frontend:       http://localhost:8080" -ForegroundColor White
Write-Host "MQTT Broker:    localhost:1883" -ForegroundColor White
Write-Host ""
try {
    Start-Process "http://localhost:8080"
} catch {
    Write-Host "Please open http://localhost:8080 in your browser" -ForegroundColor Gray
}

Write-Host "Press Enter to exit..." -ForegroundColor Gray
Read-Host