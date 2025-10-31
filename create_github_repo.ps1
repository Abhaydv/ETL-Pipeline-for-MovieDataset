# create_github_repo.ps1
# Creates a public GitHub repo using $env:GITHUB_TOKEN, sets origin, pushes, then resets origin URL.

$repoName = 'movies-etl-pipeline'
$description = 'ETL pipeline for TMDB movies; includes ETL code, tests, and CI workflow.'
$private = $false

if (-not $env:GITHUB_TOKEN) {
    Write-Error 'GITHUB_TOKEN environment variable is not set. Please set $env:GITHUB_TOKEN and re-run this script.'
    exit 1
}

$body = @{ name = $repoName; description = $description; private = $private } | ConvertTo-Json
$headers = @{ Authorization = "token $env:GITHUB_TOKEN"; Accept = 'application/vnd.github+json' }

try {
    $resp = Invoke-RestMethod -Uri 'https://api.github.com/user/repos' -Method Post -Headers $headers -Body $body -ContentType 'application/json'
} catch {
    Write-Error "Failed to create repo: $_"
    exit 1
}

$clone = $resp.clone_url
$html = $resp.html_url
Write-Output "Created repository: $($resp.full_name) -> $html"

# Add remote if not exists
try {
    git remote add origin $clone 2>$null
} catch {
    Write-Output 'Remote origin may already exist; continuing.'
}

# Temporarily set remote URL to include token for non-interactive push
$pushUrl = $clone -replace '^https://', "https://$($env:GITHUB_TOKEN)@"
git remote set-url origin $pushUrl

# Ensure main branch name and push
git branch -M main
try {
    git push -u origin main
} catch {
    Write-Error "Push failed: $_"
    # Reset origin to safe URL before exiting
    git remote set-url origin $clone
    exit 1
}

# Reset remote to clone_url (without token)
git remote set-url origin $clone

Write-Output "Successfully pushed local 'main' branch to $html"
Write-Output "NOTE: If you'd like the token removed from any local files, ensure your .git/config does not contain the token."
