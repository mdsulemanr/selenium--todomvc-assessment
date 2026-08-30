param(
    [string]$Workers = "auto",

    [ValidatePattern("^(chrome|firefox|edge)(,(chrome|firefox|edge))*$")]
    [string]$Browser = "chrome",

    [ValidatePattern("^(desktop|mobile)(,(desktop|mobile))*$")]
    [string]$Viewport = "desktop"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path "$PSScriptRoot\.."
Set-Location $repoRoot

$python = ".\.venv\Scripts\python.exe"
& $python -m pytest -n $Workers --browser $Browser --viewport $Viewport
