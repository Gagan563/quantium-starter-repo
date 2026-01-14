# Pink Morsel Sales Analysis - Automated Test Suite Runner (PowerShell)
# This script activates the virtual environment and runs the pytest test suite
# Exit codes: 0 = all tests passed, 1 = tests failed or error occurred

param(
    [switch]$NoExit = $false
)

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Pink Morsel Sales Analysis - Test Suite" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Get the script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Change to project directory
Set-Location $scriptDir

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "❌ Error: Virtual environment not found at venv/" -ForegroundColor Red
    Write-Host "Please run: python -m venv venv" -ForegroundColor Yellow
    exit 1
}

Write-Host "📦 Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# Verify pytest is installed
try {
    $pytest = & python -m pytest --version 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "pytest not found"
    }
}
catch {
    Write-Host "❌ Error: pytest not found in virtual environment" -ForegroundColor Red
    Write-Host "Please install it with: pip install pytest" -ForegroundColor Yellow
    exit 1
}

Write-Host "✓ Virtual environment activated" -ForegroundColor Green
Write-Host ""

# Run the test suite
Write-Host "🧪 Running test suite..." -ForegroundColor Yellow
Write-Host ""

& python -m pytest test_app.py -v --tb=short

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "==========================================" -ForegroundColor Green
    Write-Host "✅ All tests passed!" -ForegroundColor Green
    Write-Host "==========================================" -ForegroundColor Green
    if (-not $NoExit) {
        exit 0
    }
}
else {
    $testExitCode = $LASTEXITCODE
    Write-Host ""
    Write-Host "==========================================" -ForegroundColor Red
    Write-Host "❌ Tests failed with exit code: $testExitCode" -ForegroundColor Red
    Write-Host "==========================================" -ForegroundColor Red
    if (-not $NoExit) {
        exit 1
    }
}
