Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path "$PSScriptRoot\.."
Set-Location $repoRoot

docker compose -f docker-compose.selenium-grid.yml down
