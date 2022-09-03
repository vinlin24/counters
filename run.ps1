<# Shortcut script for common tasks #>

param (
    [Parameter()]
    [string] $TaskName
)

$PACKAGE_NAME = "counters"
$TEST_SCRIPT_PATH = "test/test.py"

<# Assert script conditions #>

$scriptPath = $MyInvocation.MyCommand.Path  # Like __file__ for PS
$scriptDir = Split-Path $scriptPath -Parent  # Split-Path returns a string
if ((Get-Location).ToString() -ne $scriptDir) {
    Write-Host "Script must be run at script's directory, aborted." -ForegroundColor Red
    exit 1
}

<# Run module task #>

function Start-RunTask {
    Write-Host "TASK: Running main module..." -ForegroundColor Yellow
    python -m $PACKAGE_NAME
}

<# Run test script task #>

function Start-TestTask {
    Write-Host "TASK: Running test script..." -ForegroundColor Yellow
    python $TEST_SCRIPT_PATH
}

<# Pre-commit checklist task #>

function Start-CommitTask {
    Write-Host "TASK: Running pre-commit checklist..." -ForegroundColor Yellow
    pip freeze | Out-File -Encoding utf8 ".\requirements.txt"
    Write-Host "Updated requirements.txt with state of current venv."
}

<# View log file #>
function Start-ViewLogTask {
    Write-Host "TASK: Opening program log file in editor..." -ForegroundColor Yellow
    code "C:\Users\soula\.config\counters\counters.log"
}

<# Main process: determine which task to run #>

switch ($TaskName) {
    "" { Start-RunTask }
    "Run" { Start-RunTask }
    "Test" { Start-TestTask }
    "Commit" { Start-CommitTask }
    "Log" { Start-ViewLogTask }
    default {
        Write-Host "Unrecognized task name, aborted." -ForegroundColor Red
        exit 1
    }
}

Write-Host "Finished running run.ps1." -ForegroundColor Green
exit 0
