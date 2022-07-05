# copytasks.ps1
# copy tasks.json in every python project
#
# 2022-07-05  PV

$root = 'C:\Development\GitHub\Python\Learning'
foreach($d in Get-ChildItem -Directory -Path $root)
{
    Write-Host($d)
    Copy-Item -Path "$root\tasks.json" -Destination "$($d.FullName)\.vscode\tasks.json" -Force   
}
