<#
.SYNOPSIS
Stop all Bella Bot services and free ports

.DESCRIPTION
This script stops all running development services by:
1. Killing processes by command line pattern
2. Killing processes by port
3. Cleaning up any temporary files

.EXAMPLE
.\stop.ps1
#>

Write-Host ""
Write-Host "================================================================" -ForegroundColor Red
Write-Host "       Stopping Bella Bot Services      " -ForegroundColor Red
Write-Host "================================================================" -ForegroundColor Red
Write-Host ""

$stopped = 0

# ============================================================================
# 1. Stop processes by command line pattern
# ============================================================================

Write-Host "Finding and stopping processes..." -ForegroundColor Yellow

$patterns = @(
    'uvicorn',
    'bella_bot',
    'vite',
    'npm run dev',
    'Lavalink.jar',
    'redis-server'
)

foreach ($pattern in $patterns) {
    try {
        $foundProcesses = Get-CimInstance Win32_Process | Where-Object { 
            $_.CommandLine -and ($_.CommandLine -match $pattern) 
        }
        
        foreach ($proc in $foundProcesses) {
            try {
                Write-Host "  Stopping PID $($proc.ProcessId) ($($proc.Name))" -ForegroundColor Gray
                Stop-Process -Id $proc.ProcessId -Force -ErrorAction Stop
                $stopped++
            }
            catch {
                Write-Host "  [WARNING] Failed to stop PID $($proc.ProcessId): $_" -ForegroundColor Yellow
            }
        }
    }
    catch {
        # Ignore errors in process enumeration
    }
}

# ============================================================================
# 2. Stop processes by port (fallback method)
# ============================================================================

Write-Host ""
Write-Host "Checking ports..." -ForegroundColor Yellow

$ports = @(
    8000,  # API
    5173,  # Vite
    3000,  # Alternative web port
    2333,  # Lavalink
    6379   # Redis
)

foreach ($port in $ports) {
    try {
        $connection = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
        if ($connection) {
            $processId = $connection.OwningProcess
            $processName = (Get-Process -Id $processId -ErrorAction SilentlyContinue).Name
            Write-Host "  Stopping process on port ${port}: PID $processId ($processName)" -ForegroundColor Gray
            Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue
            $stopped++
        }
    }
    catch {
        # Ignore if port is not in use
    }
}

# ============================================================================
# 3. Close PowerShell windows (for processes started by setup-and-run.ps1)
# ============================================================================

Write-Host ""
Write-Host "Closing service windows..." -ForegroundColor Yellow

# Try to close windows that were opened by our startup script
try {
    # Get all PowerShell windows running our commands
    $psWindows = Get-Process powershell -ErrorAction SilentlyContinue | Where-Object {
        $_.MainWindowTitle -match 'bella_bot|uvicorn|vite|npm'
    }
    
    foreach ($window in $psWindows) {
        Write-Host "  Closing window: $($window.MainWindowTitle)" -ForegroundColor Gray
        Stop-Process -Id $window.Id -Force -ErrorAction SilentlyContinue
        $stopped++
    }
}
catch {
    # Ignore errors
}

# ============================================================================
# 4. Cleanup
# ============================================================================

Write-Host ""
Write-Host "Cleaning up..." -ForegroundColor Yellow

# Remove PID files if they exist
$pidDir = Join-Path (Split-Path -Parent $MyInvocation.MyCommand.Path) 'pids'
if (Test-Path $pidDir) {
    Get-ChildItem -Path $pidDir -Filter *.pid -ErrorAction SilentlyContinue | 
    Remove-Item -Force -ErrorAction SilentlyContinue
    Write-Host "  Removed temporary PID files" -ForegroundColor Gray
}

# ============================================================================
# 5. Summary
# ============================================================================

Write-Host ""
if ($stopped -gt 0) {
    Write-Host "[OK] Stopped $stopped process(es)" -ForegroundColor Green
}
else {
    Write-Host "[INFO] No running services found" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "To verify all processes are stopped:" -ForegroundColor Yellow
Write-Host "  - Task Manager (Ctrl+Shift+Esc)" -ForegroundColor Gray
Write-Host "  - Or run: Get-Process | Where-Object Name -match 'python|node|java'" -ForegroundColor Gray
Write-Host ""
