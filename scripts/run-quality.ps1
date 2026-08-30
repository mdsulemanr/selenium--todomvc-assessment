Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path "$PSScriptRoot\.."
Set-Location $repoRoot

$python = ".\.venv\Scripts\python.exe"

& $python -m ruff check .
& $python -m pytest --collect-only -q
