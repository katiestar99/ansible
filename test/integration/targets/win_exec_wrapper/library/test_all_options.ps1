#!powershell

#Requires -Module Assible.ModuleUtils.Legacy
#Requires -Module Assible.ModuleUtils.SID
#Requires -Version 3.0
#AssibleRequires -OSVersion 6
#AssibleRequires -Become

$output = &whoami.exe
$sid = Convert-ToSID -account_name $output.Trim()

Exit-Json -obj @{ output = $sid; changed = $false }
