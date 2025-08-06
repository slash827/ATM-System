# ATM System - Automated API Testing Script
# This script replicates all the PowerShell commands we ran manually

param(
    [string]$BaseUrl = "http://localhost:8000",
    [string]$AccountNumber = "123456"
)

Write-Host "🚀 ATM System API Test Suite" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green
Write-Host "Base URL: $BaseUrl" -ForegroundColor Yellow
Write-Host "Test Account: $AccountNumber" -ForegroundColor Yellow
Write-Host ""

# Function to make API calls and display results
function Test-APIEndpoint {
    param(
        [string]$Method,
        [string]$Endpoint,
        [string]$Description,
        [hashtable]$Body = $null,
        [hashtable]$Headers = @{"Content-Type" = "application/json"}
    )
    
    Write-Host "🧪 Testing: $Description" -ForegroundColor Cyan
    Write-Host "   $Method $Endpoint" -ForegroundColor Gray
    
    try {
        $params = @{
            Uri = "$BaseUrl$Endpoint"
            Method = $Method
            Headers = $Headers
        }
        
        if ($Body) {
            $params.Body = $Body | ConvertTo-Json
        }
        
        $response = Invoke-RestMethod @params
        Write-Host "   ✅ SUCCESS" -ForegroundColor Green
        
        if ($response) {
            Write-Host "   Response: " -ForegroundColor White -NoNewline
            $response | ConvertTo-Json -Compress | Write-Host -ForegroundColor Gray
        }
        
        return $response
    }
    catch {
        Write-Host "   ❌ FAILED: $($_.Exception.Message)" -ForegroundColor Red
        return $null
    }
    finally {
        Write-Host ""
    }
}

# Test 1: Health Check
Test-APIEndpoint -Method GET -Endpoint "/health" -Description "Health Check"

# Test 2: Root Endpoint
Test-APIEndpoint -Method GET -Endpoint "/" -Description "Root Endpoint"

# Test 3: Get Initial Balance
$initialBalance = Test-APIEndpoint -Method GET -Endpoint "/accounts/$AccountNumber/balance" -Description "Get Initial Balance"

# Test 4: CORS Preflight Test
$corsHeaders = @{
    "Origin" = "http://localhost:5173"
    "Access-Control-Request-Method" = "POST"
    "Access-Control-Request-Headers" = "Content-Type"
}
Test-APIEndpoint -Method OPTIONS -Endpoint "/accounts/$AccountNumber/balance" -Description "CORS Preflight Check" -Headers $corsHeaders

# Test 5: Deposit Money
$depositResponse = Test-APIEndpoint -Method POST -Endpoint "/accounts/$AccountNumber/deposit" -Description "Deposit Money" -Body @{amount = 75.50}

# Test 6: Withdraw Money
$withdrawResponse = Test-APIEndpoint -Method POST -Endpoint "/accounts/$AccountNumber/withdraw" -Description "Withdraw Money" -Body @{amount = 25.25}

# Test 7: Check Balance After Transactions
Test-APIEndpoint -Method GET -Endpoint "/accounts/$AccountNumber/balance" -Description "Check Balance After Transactions"

# Test 8: Create Regular Time Deposit
$timeDepositResponse = Test-APIEndpoint -Method POST -Endpoint "/accounts/$AccountNumber/time-deposits" -Description "Create Regular Time Deposit" -Body @{
    amount = 200.00
    duration_months = 18
    is_test_deposit = $false
}

# Test 9: Create Test Time Deposit
$testDepositResponse = Test-APIEndpoint -Method POST -Endpoint "/accounts/$AccountNumber/time-deposits" -Description "Create Test Time Deposit" -Body @{
    amount = 50.00
    duration_months = 3
    is_test_deposit = $true
}

# Test 10: List Time Deposits
Test-APIEndpoint -Method GET -Endpoint "/accounts/$AccountNumber/time-deposits" -Description "List Time Deposits"

# Test 11: Wait and Mature Test Deposit
if ($testDepositResponse -and $testDepositResponse.deposit) {
    $depositId = $testDepositResponse.deposit.deposit_id
    Write-Host "⏰ Waiting 2 seconds for test deposit to mature..." -ForegroundColor Yellow
    Start-Sleep -Seconds 2
    
    Test-APIEndpoint -Method POST -Endpoint "/time-deposits/$depositId/mature" -Description "Mature Test Deposit" -Body @{}
}

# Test 12: Money Transfer
Test-APIEndpoint -Method POST -Endpoint "/accounts/$AccountNumber/transfer" -Description "Money Transfer" -Body @{
    amount = 30.00
    recipient_account = "789012"
    message = "Automated test transfer"
}

# Test 13: Test Error Cases
Write-Host "🔥 Testing Error Cases" -ForegroundColor Magenta
Write-Host "========================" -ForegroundColor Magenta

# Invalid account number
Test-APIEndpoint -Method GET -Endpoint "/accounts/99999/balance" -Description "Invalid Account Number"

# Negative amount
Test-APIEndpoint -Method POST -Endpoint "/accounts/$AccountNumber/deposit" -Description "Negative Amount (Expected to Fail)" -Body @{amount = -50.00}

# Amount too large
Test-APIEndpoint -Method POST -Endpoint "/accounts/$AccountNumber/deposit" -Description "Amount Too Large (Expected to Fail)" -Body @{amount = 50000.00}

# Insufficient funds (using empty account)
Test-APIEndpoint -Method POST -Endpoint "/accounts/555444/withdraw" -Description "Insufficient Funds (Expected to Fail)" -Body @{amount = 100.00}

# Test 14: Final Balance Check
$finalBalance = Test-APIEndpoint -Method GET -Endpoint "/accounts/$AccountNumber/balance" -Description "Final Balance Check"

# Summary
Write-Host "📊 TEST SUMMARY" -ForegroundColor Green
Write-Host "===============" -ForegroundColor Green

if ($initialBalance -and $finalBalance) {
    $balanceChange = $finalBalance.balance - $initialBalance.balance
    Write-Host "Initial Balance: `$$($initialBalance.balance)" -ForegroundColor White
    Write-Host "Final Balance:   `$$($finalBalance.balance)" -ForegroundColor White
    Write-Host "Net Change:      `$$balanceChange" -ForegroundColor $(if ($balanceChange -ge 0) { "Green" } else { "Red" })
}

Write-Host ""
Write-Host "🎉 API Test Suite Completed!" -ForegroundColor Green
Write-Host "Check the results above for any failures." -ForegroundColor Yellow
