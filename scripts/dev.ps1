$ErrorActionPreference = "Stop"

if (-not (Test-Path ".env")) {
  Copy-Item ".env.example" ".env"
}

docker compose up -d --build
Write-Host "Stack started. Open http://localhost:8000"
