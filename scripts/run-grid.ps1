param(
    [string]$Workers = "3",

    [ValidatePattern("^(chrome|firefox|edge)(,(chrome|firefox|edge))*$")]
    [string]$Browser = "chrome",

    [ValidatePattern("^(desktop|mobile)(,(desktop|mobile))*$")]
    [string]$Viewport = "desktop",

    [string]$RemoteUrl = "http://localhost:4444"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path "$PSScriptRoot\.."
Set-Location $repoRoot

$python = ".\.venv\Scripts\python.exe"
& $python -m pytest -n $Workers --remote-url $RemoteUrl --browser $Browser --viewport $Viewport
