param(
    [string]$Workers = "",

    [string]$Browser = "chrome",

    [string]$Viewport = "desktop"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path "$PSScriptRoot\.."
Set-Location $repoRoot

$python = ".\.venv\Scripts\python.exe"
$allureResults = "reports\allure-results"
$args = @("--alluredir", $allureResults, "--browser", $Browser, "--viewport", $Viewport)

if ($Workers) {
    $args = @("-n", $Workers) + $args
}

& $python -m pytest @args

if (Get-Command allure -ErrorAction SilentlyContinue) {
    allure generate $allureResults -o "reports\allure-report" --clean
    Write-Host "Generated Allure report at reports\allure-report"
} else {
    Write-Host "Allure results written to $allureResults"
    Write-Host "Install the Allure CLI to generate/open the HTML report."
}
