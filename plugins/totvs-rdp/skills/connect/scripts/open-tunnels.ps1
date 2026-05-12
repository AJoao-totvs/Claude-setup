#requires -Version 5.1
<#
.SYNOPSIS
  TOTVS RDP - two-hop SSH tunnel opener (Windows).

.EXAMPLE
  .\open-tunnels.ps1 -Ocid "ocid1.bastionsession..." `
                     -BastionKey "$env:USERPROFILE\.ssh\bastion.key" `
                     -ServerKey "$env:USERPROFILE\.ssh\totvs-server.key" `
                     -SshUser opc

.NOTES
  Exits 0 once both tunnels are listening. Emits two background process IDs to the success stream.
#>

[CmdletBinding()]
param(
  [Parameter(Mandatory = $true)] [string] $Ocid,
  [Parameter(Mandatory = $true)] [string] $BastionKey,
  [Parameter(Mandatory = $true)] [string] $ServerKey,
  [string] $SshUser    = 'opc',
  [int]    $LocalRdp   = 3389,
  [int]    $LocalJump  = 2222,
  [string] $ServerIp   = '10.171.89.151',
  [string] $BastionHost = 'host.bastion.sa-saopaulo-1.oci.oraclecloud.com'
)

$ErrorActionPreference = 'Stop'

function Fail([string]$msg) { Write-Error "erro: $msg"; exit 1 }

if ($Ocid -notmatch '^ocid1\.bastionsession\.oc1\.sa-saopaulo-1\.') {
  Fail 'OCID nao tem o prefixo esperado (ocid1.bastionsession.oc1.sa-saopaulo-1.)'
}
if (-not (Test-Path -LiteralPath $BastionKey)) { Fail "chave do bastion nao encontrada: $BastionKey" }
if (-not (Test-Path -LiteralPath $ServerKey))  { Fail "chave do servidor nao encontrada: $ServerKey" }

function Wait-Port {
  param([int]$Port, [int]$AttemptsMax = 10)
  for ($i = 0; $i -lt $AttemptsMax; $i++) {
    $r = Test-NetConnection -ComputerName 127.0.0.1 -Port $Port -InformationLevel Quiet -WarningAction SilentlyContinue
    if ($r) { return $true }
    Start-Sleep -Seconds 1
  }
  return $false
}

$hop1Log = New-TemporaryFile
$hop2Log = New-TemporaryFile

$hop1Args = @(
  '-i', $BastionKey, '-N',
  '-L', "${LocalJump}:${ServerIp}:22",
  '-p', '22',
  '-o', 'ServerAliveInterval=30',
  '-o', 'ServerAliveCountMax=3',
  '-o', 'StrictHostKeyChecking=accept-new',
  '-o', 'ExitOnForwardFailure=yes',
  '-E', $hop1Log.FullName,
  "${Ocid}@${BastionHost}"
)
$hop1 = Start-Process -FilePath 'ssh' -ArgumentList $hop1Args -PassThru -WindowStyle Hidden

if (-not (Wait-Port -Port $LocalJump -AttemptsMax 10)) {
  Stop-Process -Id $hop1.Id -Force -ErrorAction SilentlyContinue
  Write-Error "hop 1 nao subiu. log:`n$(Get-Content $hop1Log.FullName -Tail 20)"
  exit 2
}

$knownHosts = Join-Path $env:TEMP 'totvs_known_hosts'
$hop2Args = @(
  '-i', $ServerKey, '-p', "$LocalJump", '-N',
  '-L', "${LocalRdp}:localhost:3389",
  '-o', 'ServerAliveInterval=30',
  '-o', 'ServerAliveCountMax=3',
  '-o', 'StrictHostKeyChecking=accept-new',
  '-o', "UserKnownHostsFile=$knownHosts",
  '-o', 'ExitOnForwardFailure=yes',
  '-E', $hop2Log.FullName,
  "${SshUser}@localhost"
)
$hop2 = Start-Process -FilePath 'ssh' -ArgumentList $hop2Args -PassThru -WindowStyle Hidden

if (-not (Wait-Port -Port $LocalRdp -AttemptsMax 10)) {
  Stop-Process -Id $hop2.Id -Force -ErrorAction SilentlyContinue
  Stop-Process -Id $hop1.Id -Force -ErrorAction SilentlyContinue
  Write-Error "hop 2 nao subiu. log:`n$(Get-Content $hop2Log.FullName -Tail 20)"
  exit 3
}

Write-Output ("{0} {1}" -f $hop1.Id, $hop2.Id)
Write-Host ("tuneis ativos. porta RDP local: {0}" -f $LocalRdp) -ForegroundColor Green
