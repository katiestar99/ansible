#!powershell

# use different cases, spacing and plural of 'module' to exercise flexible powershell dialect
#ReQuiReS   -ModUleS    Assible.ModuleUtils.Legacy
#Requires -Module Assible.ModuleUtils.ValidTestModule

$o = CustomFunction

Exit-Json @{data=$o}
