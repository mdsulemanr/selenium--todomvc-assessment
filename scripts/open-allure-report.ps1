Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path "$PSScriptRoot\.."
Set-Location $repoRoot

if (-not (Get-Command allure -ErrorAction SilentlyContinue)) {
    throw "Allure CLI is not installed or not on PATH. Install it before opening the HTML report."
}

if (-not (Test-Path "reports\allure-results")) {
    throw "No Allure results found at reports\allure-results. Run .\scripts\run-allure.ps1 first."
}

allure generate "reports\allure-results" -o "reports\allure-report" --clean
allure open "reports\allure-report"
