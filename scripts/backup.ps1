$ErrorActionPreference = "Stop"

$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$dest = if ($args.Count -gt 0) { $args[0] } else { ".\\backups" }
New-Item -ItemType Directory -Force -Path $dest | Out-Null

docker compose exec -T postgres pg_dump -U ${env:POSTGRES_USER} ${env:POSTGRES_DB} | Out-File -Encoding utf8 "$dest\\db-$stamp.sql"
tar -czf "$dest\\media-$stamp.tar.gz" media

Write-Host "Backup created in $dest"
