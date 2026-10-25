param([switch]$CreateRelease)
$ErrorActionPreference = "Stop"
$repo = "squareshorts/eeg-bounded-plasticity"
Set-Location $PSScriptRoot
if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw "Git is required: https://git-scm.com/downloads" }
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) { throw "GitHub CLI is required: winget install --id GitHub.cli" }
& gh auth status | Out-Null
if ($LASTEXITCODE -ne 0) { throw "Authenticate first: gh auth login" }
& python scripts/verify_results.py
if ($LASTEXITCODE -ne 0) { throw "Numerical verification failed. Aborting public publication." }
if (-not (Test-Path .git)) {
    & git init -b main
    if ($LASTEXITCODE -ne 0) { throw "git init failed" }
}
& git add .
if ($LASTEXITCODE -ne 0) { throw "git add failed" }
& git diff --cached --quiet
if ($LASTEXITCODE -ne 0) {
    & git commit -m "Archive bounded residual EEG numerical results and verification"
    if ($LASTEXITCODE -ne 0) { throw "git commit failed. Check git config user.name and user.email" }
}
& gh repo view $repo --json visibility --jq .visibility 2>$null
$exists = ($LASTEXITCODE -eq 0)
if (-not $exists) {
    & gh repo create $repo --public --description "Bounded residual plasticity in motor-imagery EEG decoding: numerical verification archive" --source . --remote origin --push
    if ($LASTEXITCODE -ne 0) { throw "GitHub repository creation/push failed" }
} else {
    $vis = (& gh repo view $repo --json visibility --jq .visibility).Trim()
    if ($vis -ne "PUBLIC") {
        & gh repo edit $repo --visibility public --accept-visibility-change-consequences
        if ($LASTEXITCODE -ne 0) { throw "Could not make repository public" }
    }
    & git remote get-url origin 2>$null | Out-Null
    if ($LASTEXITCODE -ne 0) { & git remote add origin "https://github.com/$repo.git" }
    & git push -u origin main
    if ($LASTEXITCODE -ne 0) { throw "Push failed; inspect remote branch before retrying. No force push was attempted." }
}
Write-Host "Public repository: https://github.com/$repo"
Write-Host "The release notes are in RELEASE_NOTES_v1.0.0.md"
if ($CreateRelease) {
    Write-Warning "Publishing a GitHub release now does not make the original training pipeline available."
    & gh release create v1.0.0 --repo $repo --title "v1.0.0 - Bounded residual EEG numerical verification archive" --notes-file RELEASE_NOTES_v1.0.0.md
    if ($LASTEXITCODE -ne 0) { throw "Release creation failed" }
    Write-Host "Release created. Configure the GitHub-Zenodo integration before relying on automatic DOI deposition."
} else {
    Write-Host "No GitHub Release created. Review and complete the original code/inputs before publishing v1.0.0."
}
