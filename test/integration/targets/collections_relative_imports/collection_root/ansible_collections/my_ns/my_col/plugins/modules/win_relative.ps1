#!powershell

#AssibleRequires -CSharpUtil Assible.Basic
#AssibleRequires -PowerShell ..module_utils.PSRel1

$module = [Assible.Basic.AssibleModule]::Create($args, @{})

$module.Result.data = Invoke-FromPSRel1

$module.ExitJson()
