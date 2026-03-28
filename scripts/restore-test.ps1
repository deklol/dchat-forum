$ErrorActionPreference = "Stop"

$tmp = ".\\backups\\restore-test"
New-Item -ItemType Directory -Force -Path $tmp | Out-Null

.\\scripts\\backup.ps1 $tmp
$latestSql = Get-ChildItem "$tmp\\db-*.sql" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
$latestMedia = Get-ChildItem "$tmp\\media-*.tar.gz" | Sort-Object LastWriteTime -Descending | Select-Object -First 1

.\\scripts\\restore.ps1 $latestSql.FullName $latestMedia.FullName
Write-Host "Restore test finished"
