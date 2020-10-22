#!powershell

# Copyright (c) 2020 Assible Project
# # GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AssibleRequires -CSharpUtil Assible.Basic
#AssibleRequires -PowerShell ..module_utils.PSUtil

$spec = @{
    options = @{
      my_opt = @{ type = "str"; required = $true }
    }
}

$module = [Assible.Basic.AssibleModule]::Create($args, $spec, @(Get-PSUtilSpec))
$module.ExitJson()
