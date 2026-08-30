param(
    [ValidateSet("chrome", "firefox", "edge")]
    [string]$Browser = "chrome",

    [ValidateSet("desktop", "mobile")]
    [string]$Viewport = "desktop",

    [switch]$Headed
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path "$PSScriptRoot\.."
Set-Location $repoRoot

$python = ".\.venv\Scripts\python.exe"
$args = @("--browser", $Browser, "--viewport", $Viewport)

if ($Headed) {
    $args += "--headed"
}

& $python -m pytest @args
