#powershell

#Requires -Module Assible.ModuleUtils.Legacy

$params = Parse-Args $args

$path = Get-AssibleParam -Obj $params -Name path -Type path

Exit-Json @{ path=$path }
