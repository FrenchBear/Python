# clean.ps1
# Delete __pycache__ and .mypy_cache in every python project
#
# 2022-07-05  PV

$root = 'C:\Development\GitHub\Python\Learning'
foreach($d in Get-ChildItem -Directory -Path $root)
{
    Write-Host($d)
    if (Test-Path -Path "$($d.FullName)\__pycache__") {
        Remove-Item -Recurse -Force "$($d.FullName)\__pycache__"
    }
    if (Test-Path -Path "$($d.FullName)\.mypy_cache") {
        Remove-Item -Recurse -Force "$($d.FullName)\.mypy_cache"
    }
    if (Test-Path -Path "$($d.FullName)\.idea") {
        Remove-Item -Recurse -Force "$($d.FullName)\.idea"
    }
    if (Test-Path -Path "$($d.FullName)\.vs") {
        Remove-Item -Recurse -Force "$($d.FullName)\.vs"
    }
    if (Test-Path -Path "$($d.FullName)\.vscode\.ropeproject") {
        Remove-Item -Recurse -Force "$($d.FullName)\.vscode\.ropeproject"
    }
}
