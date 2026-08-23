[CmdletBinding()]
param(
    [switch]$StaticOnly
)

$ErrorActionPreference = 'Stop'
$expectedDigest = 'sha256:f410270e715c795b4935eb16f94c099f7aee8da81c340c9842e76f0d5e716ff3'
$composePath = Join-Path $PSScriptRoot 'compose.yaml'
$composeText = Get-Content -LiteralPath $composePath -Raw

$requiredLiterals = @(
    "docker.n8n.io/n8nio/n8n@$expectedDigest",
    '127.0.0.1:5678:5678',
    'internal: true',
    'N8N_ENCRYPTION_KEY_FILE: /run/secrets/n8n_encryption_key',
    'N8N_PUBLIC_API_DISABLED: "true"',
    'N8N_PUBLIC_API_SWAGGERUI_DISABLED: "true"',
    'EXECUTIONS_DATA_SAVE_ON_ERROR: none',
    'EXECUTIONS_DATA_SAVE_ON_SUCCESS: none',
    'n8n-nodes-base.httpRequest'
)

foreach ($literal in $requiredLiterals) {
    if (-not $composeText.Contains($literal)) {
        throw "Baseline check failed: required non-secret setting is missing: $literal"
    }
}

if ($composeText -cmatch '(?m)^\s*N8N_ENCRYPTION_KEY[ \t]*:') {
    throw 'Baseline check failed: plaintext N8N_ENCRYPTION_KEY must not be present.'
}

if ($composeText -match '(?i)hotelbeds|api\.test\.hotelbeds\.com') {
    throw 'Baseline check failed: provider configuration is not allowed in provisioning.'
}

Write-Output 'Static baseline: PASS'

if ($StaticOnly) {
    return
}

docker info *> $null
if ($LASTEXITCODE -ne 0) {
    throw 'Runtime check failed: Docker daemon is unavailable.'
}

$containerName = 'travel-poc-synthetic-n8n'
$containerId = docker ps --filter "name=^/$containerName$" --format '{{.ID}}'
if (-not $containerId) {
    throw 'Runtime check failed: expected n8n container is not running.'
}

$publishedPorts = docker port $containerName
if ($publishedPorts -notmatch '(?m)^5678/tcp -> 127\.0\.0\.1:5678$') {
    throw 'Runtime check failed: effective host listener is not loopback-only.'
}

$networkInternal = docker network inspect travel_poc_synthetic_n8n_isolated --format '{{.Internal}}'
if ($networkInternal -ne 'true') {
    throw 'Runtime check failed: isolated Docker network is not internal.'
}

$imageRef = docker inspect $containerName --format '{{.Config.Image}}'
if ($imageRef -ne "docker.n8n.io/n8nio/n8n@$expectedDigest") {
    throw 'Runtime check failed: container image digest differs from the approved pin.'
}

Write-Output 'Runtime baseline: PASS (Readiness Verify remains a separate gate)'
