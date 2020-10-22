#!powershell

# this should fail
#Requires -Module Assible.ModuleUtils.BogusModule

Exit-Json @{ data="success" }
