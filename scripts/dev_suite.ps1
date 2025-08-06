# ATM System - Complete Test & Development Suite
# This script starts servers, runs all tests, and provides a complete development environment

param(
    [switch]$SkipBackend,
    [switch]$SkipFrontend,
    [switch]$SkipTests,
    [switch]$FullSuite
)

$ErrorActionPreference = "Stop"
$OriginalLocation = Get-Location

function Write-Section {
    param([string]$Title, [string]$Color = "Green")
    Write-Host ""
    Write-Host "🔥 $Title" -ForegroundColor $Color
    Write-Host ("=" * ($Title.Length + 3)) -ForegroundColor $Color
}

function Write-Step {
    param([string]$Message)
    Write-Host "➡️  $Message" -ForegroundColor Cyan
}

function Write-Success {
    param([string]$Message)
    Write-Host "✅ $Message" -ForegroundColor Green
}

function Write-Error {
    param([string]$Message)
    Write-Host "❌ $Message" -ForegroundColor Red
}

function Test-Port {
    param([int]$Port)
    try {
        $connection = Test-NetConnection -ComputerName "localhost" -Port $Port -InformationLevel Quiet -WarningAction SilentlyContinue
        return $connection
    }
    catch {
        return $false
    }
}

Write-Section "ATM System Development Suite" "Magenta"
Write-Host "This script will set up and test the complete ATM system" -ForegroundColor Yellow
Write-Host ""

# Change to project root
Set-Location "c:\Users\gilad\Documents\GitHub\ATM-System"

# Backend Setup and Start
if (-not $SkipBackend) {
    Write-Section "Backend Setup & Launch"
    
    Write-Step "Installing Python dependencies..."
    try {
        pip install -r requirements.txt | Out-Null
        Write-Success "Python dependencies installed"
    }
    catch {
        Write-Error "Failed to install Python dependencies: $($_.Exception.Message)"
        exit 1
    }
    
    Write-Step "Starting FastAPI backend server..."
    if (Test-Port -Port 8000) {
        Write-Host "⚠️  Port 8000 already in use - backend may already be running" -ForegroundColor Yellow
    }
    else {
        # Start backend in background
        $backendJob = Start-Job -ScriptBlock {
            Set-Location "c:\Users\gilad\Documents\GitHub\ATM-System"
            python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
        }
        
        # Wait for backend to start
        $attempts = 0
        do {
            Start-Sleep -Seconds 2
            $attempts++
            $backendRunning = Test-Port -Port 8000
        } while (-not $backendRunning -and $attempts -lt 15)
        
        if ($backendRunning) {
            Write-Success "Backend server started on http://localhost:8000"
        }
        else {
            Write-Error "Failed to start backend server"
            exit 1
        }
    }
}

# Frontend Setup and Start
if (-not $SkipFrontend) {
    Write-Section "Frontend Setup & Launch"
    
    Set-Location "atm-frontend"
    
    Write-Step "Installing Node.js dependencies..."
    try {
        npm install | Out-Null
        Write-Success "Node.js dependencies installed"
    }
    catch {
        Write-Error "Failed to install Node.js dependencies: $($_.Exception.Message)"
        Set-Location $OriginalLocation
        exit 1
    }
    
    Write-Step "Starting React development server..."
    if (Test-Port -Port 5173) {
        Write-Host "⚠️  Port 5173 already in use - frontend may already be running" -ForegroundColor Yellow
    }
    else {
        # Start frontend in background
        $frontendJob = Start-Job -ScriptBlock {
            Set-Location "c:\Users\gilad\Documents\GitHub\ATM-System\atm-frontend"
            npm run dev
        }
        
        # Wait for frontend to start
        $attempts = 0
        do {
            Start-Sleep -Seconds 3
            $attempts++
            $frontendRunning = Test-Port -Port 5173
        } while (-not $frontendRunning -and $attempts -lt 15)
        
        if ($frontendRunning) {
            Write-Success "Frontend server started on http://localhost:5173"
        }
        else {
            Write-Error "Failed to start frontend server"
            Set-Location $OriginalLocation
            exit 1
        }
    }
    
    Set-Location ".."
}

# Wait for both servers to be fully ready
if (-not $SkipBackend -and -not $SkipFrontend) {
    Write-Step "Waiting for servers to initialize..."
    Start-Sleep -Seconds 5
    Write-Success "Servers ready for testing"
}

# Run Tests
if (-not $SkipTests) {
    Write-Section "Running Test Suite"
    
    # Backend Unit Tests
    Write-Step "Running backend unit tests..."
    try {
        $pytestResult = python -m pytest tests/ -v --tb=short
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Backend unit tests passed"
        }
        else {
            Write-Error "Some backend unit tests failed"
        }
    }
    catch {
        Write-Error "Failed to run backend unit tests: $($_.Exception.Message)"
    }
    
    # API Integration Tests
    Write-Step "Running API integration tests..."
    try {
        $apiTestResult = & "scripts\test_api.ps1"
        Write-Success "API integration tests completed"
    }
    catch {
        Write-Error "API integration tests failed: $($_.Exception.Message)"
    }
    
    # Frontend Tests (if available)
    if (Test-Path "atm-frontend\package.json") {
        $packageJson = Get-Content "atm-frontend\package.json" | ConvertFrom-Json
        if ($packageJson.scripts.test) {
            Write-Step "Running frontend tests..."
            try {
                Set-Location "atm-frontend"
                npm test -- --watchAll=false
                Write-Success "Frontend tests completed"
                Set-Location ".."
            }
            catch {
                Write-Error "Frontend tests failed: $($_.Exception.Message)"
                Set-Location ".."
            }
        }
    }
}

# Development Environment Info
Write-Section "Development Environment Ready" "Green"

Write-Host "🌐 Access Points:" -ForegroundColor White
if (-not $SkipBackend) {
    Write-Host "   • Backend API:    http://localhost:8000" -ForegroundColor Cyan
    Write-Host "   • API Docs:       http://localhost:8000/docs" -ForegroundColor Cyan
}
if (-not $SkipFrontend) {
    Write-Host "   • Frontend App:   http://localhost:5173" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "📚 Useful Commands:" -ForegroundColor White
Write-Host "   • Run tests:              .\scripts\run_tests.py" -ForegroundColor Gray
Write-Host "   • API tests only:         .\scripts\test_api.ps1" -ForegroundColor Gray
Write-Host "   • View backend logs:      Get-Job | Receive-Job" -ForegroundColor Gray
Write-Host "   • Stop servers:           Get-Job | Stop-Job; Get-Job | Remove-Job" -ForegroundColor Gray

Write-Host ""
Write-Host "🔧 Quick Test Account:" -ForegroundColor White
Write-Host "   • Account Number: 123456" -ForegroundColor Gray
Write-Host "   • Pin:           1234" -ForegroundColor Gray

if ($FullSuite) {
    Write-Host ""
    Write-Host "⚡ Running full feature demonstration..." -ForegroundColor Yellow
    
    Write-Step "Creating test account and performing transactions..."
    Start-Sleep -Seconds 2
    
    # Demonstrate key features
    $baseUrl = "http://localhost:8000"
    $account = "123456"
    
    Write-Host "   💰 Initial balance check..." -ForegroundColor Gray
    try {
        $balance = Invoke-RestMethod -Uri "$baseUrl/accounts/$account/balance" -Method GET
        Write-Host "      Balance: `$$($balance.balance)" -ForegroundColor Green
    }
    catch {
        Write-Host "      Failed to get balance" -ForegroundColor Red
    }
    
    Write-Host "   💸 Making deposit..." -ForegroundColor Gray
    try {
        $deposit = Invoke-RestMethod -Uri "$baseUrl/accounts/$account/deposit" -Method POST -Body (@{amount = 100.00} | ConvertTo-Json) -ContentType "application/json"
        Write-Host "      Deposited `$100.00" -ForegroundColor Green
    }
    catch {
        Write-Host "      Failed to make deposit" -ForegroundColor Red
    }
    
    Write-Host "   ⏰ Creating test time deposit..." -ForegroundColor Gray
    try {
        $timeDeposit = Invoke-RestMethod -Uri "$baseUrl/accounts/$account/time-deposits" -Method POST -Body (@{amount = 25.00; duration_months = 3; is_test_deposit = $true} | ConvertTo-Json) -ContentType "application/json"
        Write-Host "      Created test time deposit: `$25.00" -ForegroundColor Green
        
        Write-Host "   ⏱️  Waiting for test deposit to mature..." -ForegroundColor Gray
        Start-Sleep -Seconds 2
        
        $depositId = $timeDeposit.deposit.deposit_id
        $matured = Invoke-RestMethod -Uri "$baseUrl/time-deposits/$depositId/mature" -Method POST -Body (@{} | ConvertTo-Json) -ContentType "application/json"
        Write-Host "      Matured deposit with interest: `$$($matured.final_amount)" -ForegroundColor Green
    }
    catch {
        Write-Host "      Failed to create/mature time deposit" -ForegroundColor Red
    }
}

Write-Host ""
Write-Success "ATM System is ready for development and testing!"
Write-Host "Press Ctrl+C to stop the servers when done." -ForegroundColor Yellow

# Keep script running if servers were started
if ((-not $SkipBackend -or -not $SkipFrontend) -and -not $FullSuite) {
    Write-Host ""
    Write-Host "⌛ Servers are running... Press Ctrl+C to stop." -ForegroundColor Yellow
    try {
        while ($true) {
            Start-Sleep -Seconds 30
            # Optional: Health check
            if (-not $SkipBackend -and (Test-Port -Port 8000)) {
                Write-Host "." -NoNewline -ForegroundColor Green
            }
        }
    }
    catch {
        Write-Host ""
        Write-Host "🛑 Stopping servers..." -ForegroundColor Yellow
        Get-Job | Stop-Job
        Get-Job | Remove-Job
        Write-Success "Servers stopped"
    }
}

Set-Location $OriginalLocation
