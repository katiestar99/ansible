#1powershell

#Requires -Module Assible.ModuleUtils.Legacy
#AssibleRequires -CSharpUtil Assible.Test

$result = @{
    res = [Assible.Test.OutputTest]::GetString()
    changed = $false
}

Exit-Json -obj $result

