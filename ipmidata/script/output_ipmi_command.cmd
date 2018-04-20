@SETLOCAL ENABLEEXTENSIONS ENABLEDELAYEDEXPANSION
@ECHO OFF

:main
    SET ipmicmd=
    FOR /F "tokens=*" %%a in (..\ipmicmd.txt) do (
        ECHO # >> ipmi_cmd_output.txt
        ECHO # IPMITool %%a >> ipmi_cmd_output.txt
        ECHO # >> ipmi_cmd_output.txt
        ipmitool -H 192.168.1.101 -U admin -P admin -I lanplus %%a >> ipmi_cmd_output.txt 2>&1
        ECHO. >> ipmi_cmd_output.txt
    )
@ENDLOCAL