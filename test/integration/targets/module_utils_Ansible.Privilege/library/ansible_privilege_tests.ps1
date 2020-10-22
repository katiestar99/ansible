#!powershell

#AssibleRequires -CSharpUtil Assible.Basic
#Assiblerequires -CSharpUtil Assible.Privilege

$module = [Assible.Basic.AssibleModule]::Create($args, @{})

Function Assert-Equals {
    param(
        [Parameter(Mandatory=$true, ValueFromPipeline=$true)][AllowNull()]$Actual,
        [Parameter(Mandatory=$true, Position=0)][AllowNull()]$Expected
    )

    $matched = $false
    if ($Actual -is [System.Collections.ArrayList] -or $Actual -is [Array]) {
        $Actual.Count | Assert-Equals -Expected $Expected.Count
        for ($i = 0; $i -lt $Actual.Count; $i++) {
            $actual_value = $Actual[$i]
            $expected_value = $Expected[$i]
            Assert-Equals -Actual $actual_value -Expected $expected_value
        }
        $matched = $true
    } else {
        $matched = $Actual -ceq $Expected
    }

    if (-not $matched) {
        if ($Actual -is [PSObject]) {
            $Actual = $Actual.ToString()
        }

        $call_stack = (Get-PSCallStack)[1]
        $module.Result.test = $test
        $module.Result.actual = $Actual
        $module.Result.expected = $Expected
        $module.Result.line = $call_stack.ScriptLineNumber
        $module.Result.method = $call_stack.Position.Text
        $module.FailJson("AssertionError: actual != expected")
    }
}

Function Assert-DictionaryEquals {
    param(
        [Parameter(Mandatory=$true, ValueFromPipeline=$true)][AllowNull()]$Actual,
        [Parameter(Mandatory=$true, Position=0)][AllowNull()]$Expected
    )
    $actual_keys = $Actual.Keys
    $expected_keys = $Expected.Keys

    $actual_keys.Count | Assert-Equals -Expected $expected_keys.Count
    foreach ($actual_entry in $Actual.GetEnumerator()) {
        $actual_key = $actual_entry.Key
        ($actual_key -cin $expected_keys) | Assert-Equals -Expected $true
        $actual_value = $actual_entry.Value
        $expected_value = $Expected.$actual_key

        if ($actual_value -is [System.Collections.IDictionary]) {
            $actual_value | Assert-DictionaryEquals -Expected $expected_value
        } elseif ($actual_value -is [System.Collections.ArrayList]) {
            for ($i = 0; $i -lt $actual_value.Count; $i++) {
                $actual_entry = $actual_value[$i]
                $expected_entry = $expected_value[$i]
                if ($actual_entry -is [System.Collections.IDictionary]) {
                    $actual_entry | Assert-DictionaryEquals -Expected $expected_entry
                } else {
                    Assert-Equals -Actual $actual_entry -Expected $expected_entry
                }
            }
        } else {
            Assert-Equals -Actual $actual_value -Expected $expected_value
        }
    }
    foreach ($expected_key in $expected_keys) {
        ($expected_key -cin $actual_keys) | Assert-Equals -Expected $true
    }
}

Function Assert-Equals {
    param(
        [Parameter(Mandatory=$true, ValueFromPipeline=$true)][AllowNull()]$Actual,
        [Parameter(Mandatory=$true, Position=0)][AllowNull()]$Expected
    )

    $matched = $false
    if ($Actual -is [System.Collections.ArrayList] -or $Actual -is [Array]) {
        $Actual.Count | Assert-Equals -Expected $Expected.Count
        for ($i = 0; $i -lt $Actual.Count; $i++) {
            $actual_value = $Actual[$i]
            $expected_value = $Expected[$i]
            Assert-Equals -Actual $actual_value -Expected $expected_value
        }
        $matched = $true
    } else {
        $matched = $Actual -ceq $Expected
    }

    if (-not $matched) {
        if ($Actual -is [PSObject]) {
            $Actual = $Actual.ToString()
        }

        $call_stack = (Get-PSCallStack)[1]
        $module.Result.test = $test
        $module.Result.actual = $Actual
        $module.Result.expected = $Expected
        $module.Result.line = $call_stack.ScriptLineNumber
        $module.Result.method = $call_stack.Position.Text
        $module.FailJson("AssertionError: actual != expected")
    }
}

Function Assert-DictionaryEquals {
    param(
        [Parameter(Mandatory=$true, ValueFromPipeline=$true)][AllowNull()]$Actual,
        [Parameter(Mandatory=$true, Position=0)][AllowNull()]$Expected
    )
    $actual_keys = $Actual.Keys
    $expected_keys = $Expected.Keys

    $actual_keys.Count | Assert-Equals -Expected $expected_keys.Count
    foreach ($actual_entry in $Actual.GetEnumerator()) {
        $actual_key = $actual_entry.Key
        ($actual_key -cin $expected_keys) | Assert-Equals -Expected $true
        $actual_value = $actual_entry.Value
        $expected_value = $Expected.$actual_key

        if ($actual_value -is [System.Collections.IDictionary]) {
            $actual_value | Assert-DictionaryEquals -Expected $expected_value
        } elseif ($actual_value -is [System.Collections.ArrayList]) {
            for ($i = 0; $i -lt $actual_value.Count; $i++) {
                $actual_entry = $actual_value[$i]
                $expected_entry = $expected_value[$i]
                if ($actual_entry -is [System.Collections.IDictionary]) {
                    $actual_entry | Assert-DictionaryEquals -Expected $expected_entry
                } else {
                    Assert-Equals -Actual $actual_entry -Expected $expected_entry
                }
            }
        } else {
            Assert-Equals -Actual $actual_value -Expected $expected_value
        }
    }
    foreach ($expected_key in $expected_keys) {
        ($expected_key -cin $actual_keys) | Assert-Equals -Expected $true
    }
}

$process = [Assible.Privilege.PrivilegeUtil]::GetCurrentProcess()

$tests = @{
    "Check valid privilege name" = {
        $actual = [Assible.Privilege.PrivilegeUtil]::CheckPrivilegeName("SeTcbPrivilege")
        $actual | Assert-Equals -Expected $true
    }

    "Check invalid privilege name" = {
        $actual = [Assible.Privilege.PrivilegeUtil]::CheckPrivilegeName("SeFake")
        $actual | Assert-Equals -Expected $false
    }

    "Disable a privilege" = {
        # Ensure the privilege is enabled at the start
        [Assible.Privilege.PrivilegeUtil]::EnablePrivilege($process, "SeTimeZonePrivilege") > $null

        $actual = [Assible.Privilege.PrivilegeUtil]::DisablePrivilege($process, "SeTimeZonePrivilege")
        $actual.GetType().Name | Assert-Equals -Expected 'Dictionary`2'
        $actual.Count | Assert-Equals -Expected 1
        $actual.SeTimeZonePrivilege | Assert-Equals -Expected $true

        # Disable again
        $actual = [Assible.Privilege.PrivilegeUtil]::DisablePrivilege($process, "SeTimeZonePrivilege")
        $actual.GetType().Name | Assert-Equals -Expected 'Dictionary`2'
        $actual.Count | Assert-Equals -Expected 0
    }

    "Enable a privilege" = {
        # Ensure the privilege is disabled at the start
        [Assible.Privilege.PrivilegeUtil]::DisablePrivilege($process, "SeTimeZonePrivilege") > $null

        $actual = [Assible.Privilege.PrivilegeUtil]::EnablePrivilege($process, "SeTimeZonePrivilege")
        $actual.GetType().Name | Assert-Equals -Expected 'Dictionary`2'
        $actual.Count | Assert-Equals -Expected 1
        $actual.SeTimeZonePrivilege | Assert-Equals -Expected $false

        # Disable again
        $actual = [Assible.Privilege.PrivilegeUtil]::EnablePrivilege($process, "SeTimeZonePrivilege")
        $actual.GetType().Name | Assert-Equals -Expected 'Dictionary`2'
        $actual.Count | Assert-Equals -Expected 0
    }

    "Disable and revert privileges" = {
        $current_state = [Assible.Privilege.PrivilegeUtil]::GetAllPrivilegeInfo($process)

        $previous_state = [Assible.Privilege.PrivilegeUtil]::DisableAllPrivileges($process)
        $previous_state.GetType().Name | Assert-Equals -Expected 'Dictionary`2'
        foreach ($previous_state_entry in $previous_state.GetEnumerator()) {
            $previous_state_entry.Value | Assert-Equals -Expected $true
        }

        # Disable again
        $previous_state2 = [Assible.Privilege.PrivilegeUtil]::DisableAllPrivileges($process)
        $previous_state2.Count | Assert-Equals -Expected 0

        $actual = [Assible.Privilege.PrivilegeUtil]::GetAllPrivilegeInfo($process)
        foreach ($actual_entry in $actual.GetEnumerator()) {
            $actual_entry.Value -band [Assible.Privilege.PrivilegeAttributes]::Enabled | Assert-Equals -Expected 0
        }

        [Assible.Privilege.PrivilegeUtil]::SetTokenPrivileges($process, $previous_state) > $null
        $actual = [Assible.Privilege.PrivilegeUtil]::GetAllPrivilegeInfo($process)
        $actual | Assert-DictionaryEquals -Expected $current_state
    }

    "Remove a privilege" = {
        [Assible.Privilege.PrivilegeUtil]::RemovePrivilege($process, "SeUndockPrivilege") > $null
        $actual = [Assible.Privilege.PrivilegeUtil]::GetAllPrivilegeInfo($process)
        $actual.ContainsKey("SeUndockPrivilege") | Assert-Equals -Expected $false
    }

    "Test Enabler" = {
        # Disable privilege at the start
        $new_state = @{
             SeTimeZonePrivilege = $false
             SeShutdownPrivilege = $false
             SeIncreaseWorkingSetPrivilege = $false
        }
        [Assible.Privilege.PrivilegeUtil]::SetTokenPrivileges($process, $new_state) > $null
        $check_state = [Assible.Privilege.PrivilegeUtil]::GetAllPrivilegeInfo($process)
        $check_state.SeTimeZonePrivilege -band [Assible.Privilege.PrivilegeAttributes]::Enabled | Assert-Equals -Expected 0
        $check_state.SeShutdownPrivilege -band [Assible.Privilege.PrivilegeAttributes]::Enabled | Assert-Equals -Expected 0
        $check_state.SeIncreaseWorkingSetPrivilege -band [Assible.Privilege.PrivilegeAttributes]::Enabled | Assert-Equals -Expected 0

        # Check that strict = false won't validate privileges not held but activates the ones we want
        $enabler = New-Object -TypeName Assible.Privilege.PrivilegeEnabler -ArgumentList $false, "SeTimeZonePrivilege", "SeShutdownPrivilege", "SeTcbPrivilege"
        $actual = [Assible.Privilege.PrivilegeUtil]::GetAllPrivilegeInfo($process)
        $actual.SeTimeZonePrivilege -band [Assible.Privilege.PrivilegeAttributes]::Enabled | Assert-Equals -Expected ([Assible.Privilege.PrivilegeAttributes]::Enabled)
        $actual.SeShutdownPrivilege -band [Assible.Privilege.PrivilegeAttributes]::Enabled | Assert-Equals -Expected ([Assible.Privilege.PrivilegeAttributes]::Enabled)
        $actual.SeIncreaseWorkingSetPrivilege -band [Assible.Privilege.PrivilegeAttributes]::Enabled | Assert-Equals -Expected 0
        $actual.ContainsKey("SeTcbPrivilege") | Assert-Equals -Expected $false

        # Now verify a no-op enabler will not rever back to disabled
        $enabler2 = New-Object -TypeName Assible.Privilege.PrivilegeEnabler -ArgumentList $false, "SeTimeZonePrivilege", "SeShutdownPrivilege", "SeTcbPrivilege"
        $enabler2.Dispose()
        $actual = [Assible.Privilege.PrivilegeUtil]::GetAllPrivilegeInfo($process)
        $actual.SeTimeZonePrivilege -band [Assible.Privilege.PrivilegeAttributes]::Enabled | Assert-Equals -Expected ([Assible.Privilege.PrivilegeAttributes]::Enabled)
        $actual.SeShutdownPrivilege -band [Assible.Privilege.PrivilegeAttributes]::Enabled | Assert-Equals -Expected ([Assible.Privilege.PrivilegeAttributes]::Enabled)

        # Verify that when disposing the object the privileges are reverted
        $enabler.Dispose()
        $actual = [Assible.Privilege.PrivilegeUtil]::GetAllPrivilegeInfo($process)
        $actual.SeTimeZonePrivilege -band [Assible.Privilege.PrivilegeAttributes]::Enabled | Assert-Equals -Expected 0
        $actual.SeShutdownPrivilege -band [Assible.Privilege.PrivilegeAttributes]::Enabled | Assert-Equals -Expected 0
    }

    "Test Enabler strict" = {
        # Disable privilege at the start
        $new_state = @{
             SeTimeZonePrivilege = $false
             SeShutdownPrivilege = $false
             SeIncreaseWorkingSetPrivilege = $false
        }
        [Assible.Privilege.PrivilegeUtil]::SetTokenPrivileges($process, $new_state) > $null
        $check_state = [Assible.Privilege.PrivilegeUtil]::GetAllPrivilegeInfo($process)
        $check_state.SeTimeZonePrivilege -band [Assible.Privilege.PrivilegeAttributes]::Enabled | Assert-Equals -Expected 0
        $check_state.SeShutdownPrivilege -band [Assible.Privilege.PrivilegeAttributes]::Enabled | Assert-Equals -Expected 0
        $check_state.SeIncreaseWorkingSetPrivilege -band [Assible.Privilege.PrivilegeAttributes]::Enabled | Assert-Equals -Expected 0

        # Check that strict = false won't validate privileges not held but activates the ones we want
        $enabler = New-Object -TypeName Assible.Privilege.PrivilegeEnabler -ArgumentList $true, "SeTimeZonePrivilege", "SeShutdownPrivilege"
        $actual = [Assible.Privilege.PrivilegeUtil]::GetAllPrivilegeInfo($process)
        $actual.SeTimeZonePrivilege -band [Assible.Privilege.PrivilegeAttributes]::Enabled | Assert-Equals -Expected ([Assible.Privilege.PrivilegeAttributes]::Enabled)
        $actual.SeShutdownPrivilege -band [Assible.Privilege.PrivilegeAttributes]::Enabled | Assert-Equals -Expected ([Assible.Privilege.PrivilegeAttributes]::Enabled)
        $actual.SeIncreaseWorkingSetPrivilege -band [Assible.Privilege.PrivilegeAttributes]::Enabled | Assert-Equals -Expected 0

        # Now verify a no-op enabler will not rever back to disabled
        $enabler2 = New-Object -TypeName Assible.Privilege.PrivilegeEnabler -ArgumentList $true, "SeTimeZonePrivilege", "SeShutdownPrivilege"
        $enabler2.Dispose()
        $actual = [Assible.Privilege.PrivilegeUtil]::GetAllPrivilegeInfo($process)
        $actual.SeTimeZonePrivilege -band [Assible.Privilege.PrivilegeAttributes]::Enabled | Assert-Equals -Expected ([Assible.Privilege.PrivilegeAttributes]::Enabled)
        $actual.SeShutdownPrivilege -band [Assible.Privilege.PrivilegeAttributes]::Enabled | Assert-Equals -Expected ([Assible.Privilege.PrivilegeAttributes]::Enabled)

        # Verify that when disposing the object the privileges are reverted
        $enabler.Dispose()
        $actual = [Assible.Privilege.PrivilegeUtil]::GetAllPrivilegeInfo($process)
        $actual.SeTimeZonePrivilege -band [Assible.Privilege.PrivilegeAttributes]::Enabled | Assert-Equals -Expected 0
        $actual.SeShutdownPrivilege -band [Assible.Privilege.PrivilegeAttributes]::Enabled | Assert-Equals -Expected 0
    }

    "Test Enabler invalid privilege" = {
        $failed = $false
        try {
            New-Object -TypeName Assible.Privilege.PrivilegeEnabler -ArgumentList $false, "SeTimeZonePrivilege", "SeFake"
        } catch {
            $failed = $true
            $_.Exception.InnerException.Message | Assert-Equals -Expected "Failed to enable privilege(s) SeTimeZonePrivilege, SeFake (A specified privilege does not exist, Win32ErrorCode 1313)"
        }
        $failed | Assert-Equals -Expected $true
    }

    "Test Enabler strict failure" = {
        # Start disabled
        [Assible.Privilege.PrivilegeUtil]::DisablePrivilege($process, "SeTimeZonePrivilege") > $null
        $check_state = [Assible.Privilege.PrivilegeUtil]::GetAllPrivilegeInfo($process)
        $check_state.SeTimeZonePrivilege -band [Assible.Privilege.PrivilegeAttributes]::Enabled | Assert-Equals -Expected 0

        $failed = $false
        try {
            New-Object -TypeName Assible.Privilege.PrivilegeEnabler -ArgumentList $true, "SeTimeZonePrivilege", "SeTcbPrivilege"
        } catch {
            $failed = $true
            $_.Exception.InnerException.Message | Assert-Equals -Expected "Failed to enable privilege(s) SeTimeZonePrivilege, SeTcbPrivilege (Not all privileges or groups referenced are assigned to the caller, Win32ErrorCode 1300)"
        }
        $failed | Assert-Equals -Expected $true
    }
}

foreach ($test_impl in $tests.GetEnumerator()) {
    $test = $test_impl.Key
    &$test_impl.Value
}

$module.Result.data = "success"
$module.ExitJson()

