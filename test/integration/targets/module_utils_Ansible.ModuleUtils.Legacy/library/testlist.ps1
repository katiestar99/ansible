#powershell

#Requires -Module Assible.ModuleUtils.Legacy

$params = Parse-Args $args
$value = Get-AssibleParam -Obj $params -Name value -Type list

if ($value -isnot [array]) {
    Fail-Json -obj @{} -message "value was not a list but was $($value.GetType().FullName)"
}

Exit-Json @{ count = $value.Count }
