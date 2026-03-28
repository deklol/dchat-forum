$ErrorActionPreference = "Stop"

if ($args.Count -lt 2) {
  throw "Usage: .\\scripts\\restore.ps1 <sql_file> <media_archive>"
}

$sqlFile = $args[0]
$mediaArchive = $args[1]

if (!(Test-Path $sqlFile)) { throw "Missing SQL file: $sqlFile" }
if (!(Test-Path $mediaArchive)) { throw "Missing media archive: $mediaArchive" }

Get-Content $sqlFile | docker compose exec -T postgres psql -U ${env:POSTGRES_USER} ${env:POSTGRES_DB}
tar -xzf $mediaArchive

Write-Host "Restore complete"
