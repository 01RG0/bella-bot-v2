<#
.SYNOPSIS
Setup and run Bella Bot - Complete setup and launch script

.DESCRIPTION
This script will:
1. Check prerequisites (Python, Node.js)
2. Install all dependencies
3. Validate .env configuration
4. Launch all services (API, Bot, Frontend)

.PARAMETER SkipInstall
Skip dependency installation if already installed

.EXAMPLE
.\setup-and-run.ps1
.\setup-and-run.ps1 -SkipInstall
#>

param(
    [switch]$SkipInstall
)

$ErrorActionPreference = 'Stop'

# Get repository root
$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "        Bella Bot Setup & Run          " -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# ============================================================================
# 1. Check Prerequisites
# ============================================================================

Write-Host "Checking prerequisites..." -ForegroundColor Yellow

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] Python: $pythonVersion" -ForegroundColor Green
}
catch {
    Write-Host "[ERROR] Python not found on PATH" -ForegroundColor Red
    Write-Host "   Install Python 3.11+ from https://python.org" -ForegroundColor Yellow
    exit 1
}

# Check Node.js
try {
    $nodeVersion = node --version 2>&1
    Write-Host "[OK] Node.js: $nodeVersion" -ForegroundColor Green
}
catch {
    Write-Host "[ERROR] Node.js not found on PATH" -ForegroundColor Red
    Write-Host "   Install Node.js from https://nodejs.org" -ForegroundColor Yellow
    exit 1
}

# ============================================================================
# 2. Install Dependencies
# ============================================================================

if (-not $SkipInstall) {
    Write-Host ""
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    
    # Install Python dependencies
    Write-Host ""
    Write-Host "  Installing Python packages..." -ForegroundColor Gray
    $botDir = Join-Path $repoRoot 'bot'
    Push-Location $botDir
    try {
        # Ensure __init__.py files exist
        $init1 = Join-Path $botDir 'bot\__init__.py'
        $init2 = Join-Path $botDir 'bella_bot\__init__.py'
        
        if (-not (Test-Path $init1)) {
            New-Item -Path $init1 -ItemType File -Force | Out-Null
        }
        if (-not (Test-Path $init2)) {
            New-Item -Path $init2 -ItemType File -Force | Out-Null
        }
        
        # Upgrade pip tools
        python -m pip install --upgrade pip setuptools wheel --quiet
        
        # Install bot package
        python -m pip install -e . --quiet
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  [OK] Python dependencies installed" -ForegroundColor Green
        }
        else {
            throw "Failed to install Python dependencies"
        }
    }
    catch {
        Write-Host "  [ERROR] Error installing Python dependencies: $_" -ForegroundColor Red
        exit 1
    }
    finally {
        Pop-Location
    }
    
    # Install Node.js dependencies
    Write-Host ""
    Write-Host "  Installing Node.js packages..." -ForegroundColor Gray
    $webDir = Join-Path $repoRoot 'web'
    Push-Location $webDir
    try {
        npm install --silent
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  [OK] Node.js dependencies installed" -ForegroundColor Green
        }
        else {
            throw "Failed to install Node.js dependencies"
        }
    }
    catch {
        Write-Host "  [ERROR] Error installing Node.js dependencies: $_" -ForegroundColor Red
        exit 1
    }
    finally {
        Pop-Location
    }
}
else {
    Write-Host ""
    Write-Host "Skipping installation (using existing packages)" -ForegroundColor Yellow
}

# ============================================================================
# 3. Validate Environment Configuration
# ============================================================================

Write-Host ""
Write-Host "Validating environment configuration..." -ForegroundColor Yellow

$envFile = Join-Path $repoRoot '.env'
$envExampleFile = Join-Path $repoRoot '.env.example'

# Create .env from example if missing
if (-not (Test-Path $envFile)) {
    if (Test-Path $envExampleFile) {
        Copy-Item $envExampleFile $envFile
        Write-Host "  [INFO] Created .env from .env.example" -ForegroundColor Cyan
        Write-Host "  [WARNING] Please edit .env with your Discord credentials" -ForegroundColor Yellow
        Write-Host ""
        pause
    }
    else {
        Write-Host "  [ERROR] .env and .env.example not found!" -ForegroundColor Red
        exit 1
    }
}

# Load .env into environment
Get-Content $envFile | ForEach-Object {
    if ($_ -and -not $_.StartsWith("#") -and $_.Contains("=")) {
        $key, $value = $_.Split('=', 2)
        if ($key -and $value) {
            [Environment]::SetEnvironmentVariable($key.Trim(), $value.Trim(), 'Process')
        }
    }
}

# Validate required variables
$requiredVars = @(
    'DISCORD_TOKEN',
    'VITE_DISCORD_CLIENT_ID',
    'VITE_DISCORD_REDIRECT_URI'
)

$missingVars = @()
foreach ($var in $requiredVars) {
    $val = [Environment]::GetEnvironmentVariable($var, 'Process')
    if (-not $val -or $val -eq "your_discord_bot_token" -or $val -eq "your_discord_client_id") {
        $missingVars += $var
        Write-Host "  [ERROR] Missing or invalid: $var" -ForegroundColor Red
    }
    else {
        $masked = if ($val.Length -gt 10) { "$($val.Substring(0,10))..." } else { "***" }
        Write-Host "  [OK] $var = $masked" -ForegroundColor Green
    }
}

if ($missingVars.Count -gt 0) {
    Write-Host ""
    Write-Host "[WARNING] Missing required environment variables!" -ForegroundColor Yellow
    Write-Host "   Edit $envFile and set: $($missingVars -join ', ')" -ForegroundColor Yellow
    Write-Host ""
    pause
    exit 1
}

# ============================================================================
# 4. Launch Services
# ============================================================================

Write-Host ""
Write-Host "Launching services..." -ForegroundColor Cyan
Write-Host ""

$botPath = Join-Path $repoRoot 'bot'
$webPath = Join-Path $repoRoot 'web'

# Determine uvicorn command
$uvicornCmd = Get-Command uvicorn -ErrorAction SilentlyContinue
if ($uvicornCmd) {
    $apiCmd = "uvicorn bella_bot.api_server:app --reload --host 0.0.0.0 --port 8000"
}
else {
    $apiCmd = "python -m uvicorn bella_bot.api_server:app --reload --host 0.0.0.0 --port 8000"
}

# Launch API
Write-Host "  Starting API server..." -ForegroundColor Gray
$apiScriptBlock = "Set-Location '$botPath'; $apiCmd"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $apiScriptBlock -WindowStyle Normal
Start-Sleep -Seconds 2

# Launch Discord Bot
Write-Host "  Starting Discord bot..." -ForegroundColor Gray
$botScriptBlock = "Set-Location '$botPath'; python -m bella_bot"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $botScriptBlock -WindowStyle Normal
Start-Sleep -Seconds 2

# Launch Frontend
Write-Host "  Starting frontend..." -ForegroundColor Gray
$webScriptBlock = "Set-Location '$webPath'; npm run dev"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $webScriptBlock -WindowStyle Normal

Write-Host ""
Write-Host "================================================================" -ForegroundColor Green
Write-Host "          Services Launched Successfully!            " -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Frontend:  http://localhost:5173" -ForegroundColor Cyan
Write-Host "API:       http://localhost:8000" -ForegroundColor Cyan
Write-Host "Bot:       Running in background" -ForegroundColor Cyan
Write-Host ""
Write-Host "To stop all services, run: .\stop.ps1" -ForegroundColor Yellow
Write-Host ""
