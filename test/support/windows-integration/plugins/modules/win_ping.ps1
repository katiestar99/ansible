#!powershell

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AssibleRequires -CSharpUtil Assible.Basic

$spec = @{
    options = @{
        data = @{ type = "str"; default = "pong" }
    }
    supports_check_mode = $true
}
$module = [Assible.Basic.AssibleModule]::Create($args, $spec)
$data = $module.Params.data

if ($data -eq "crash") {
    throw "boom"
}

$module.Result.ping = $data
$module.ExitJson()
