	@SETLOCAL ENABLEEXTENSIONS ENABLEDELAYEDEXPANSION
	@ECHO OFF
	IF DEFINED _DEBUG @ECHO ON
	
	SET PRGDIR=%~dp0
	SET PROGRAM=%~f0
	PUSHD %PRGDIR%

	CALL settings.cmd

	SET starttime=
	SET starttime_slot=
	SET registertimes=
	CALL :Set_Time

	IF "%1" EQU "" (
		DEL output\?????? >nul 2>nul
		REM CALL :Generate_Plan
		CALL :Loop_Manager
		pause
		GOTO :end
	)

	CALL :%1
	GOTO :end
	
:Loop_Manager
	%PYTHON% Loop_Manager.py
	GOTO :EOF 

::Generate_Server  CYCLETIME   -
:Generate_Server
	REM ECHO Generate_Server
	CALL :Exec_SQL "USE server_management; call select_server_info_list();" "%SERVERLISTFILE%.bak"
	CALL :Remove_Head "%SERVERLISTFILE%"
	GOTO :EOF

::Generate_Plan    CYCLETIME   -
:Generate_Plan
	SET linehead=
	SET modvalue=
	SET subfun=
	SET filter=
	
	CALL :Set_Round_Time
	IF DEFINED _VERBOSE (
		ECHO Generate %starttime_slot% slot...
	)
	
	DEL %WORKDIR%\%starttime_slot%.bak > nul 2>nul
	
	FOR /L %%S IN (1, 1, %CYCLETIME%) DO (
		CALL :Set_Round_Base_Time %%S
		FOR /F "tokens=1,2,3*" %%F IN ('FINDSTR /ir ^^^^:: %PROGRAM%') DO (
			SET linehead=%%F
			SET linehead=!linehead:~0,2!
			SET modtime=%%G
			IF "modtime" EQU "CYCLETIME" SET modtime=%CYCLETIME%
			SET /A modvalue = %%S %% !modtime!
			IF "!modvalue!" EQU "0" (
				SET subfun=%%F
				SET subfun=!subfun:~2!
				SET filter=%%H
				IF DEFINED _VERBOSE (
					ECHO !starttime! !subfun!
				)
				ECHO !starttime! !subfun! >> "%WORKDIR%\%starttime_slot%.bak"
			)
		)
	)
	COPY /Y "%WORKDIR%\%starttime_slot%.bak" "%WORKDIR%\%starttime_slot%" >nul 2>nul
	IF NOT DEFINED _NODELETE (
		DEL "%WORKDIR%\%starttime_slot%.bak" >nul 2>nul
	)
	GOTO :EOF

::sdr_list          10    *
:sdr_list
::sel_save_$time    30    *
:sel_save_$time
::mc_info           30    *
:mc_info
::lan_print         30    *
:lan_print
::fru               30    *
:fru
::chassis_status     5    *
:chassis_status
	SET subfun=%0
	SET subfun=%subfun:~1%
	CALL :ForEach_Server %subfun%
	GOTO :EOF
	
:_sdr_list
:_mc_info
:_lan_print
:_fru
:_chassis_status
	SET _label=%0
	SET _label=%_label:~2%
	SET _cmd=%_label:_= %

	CALL :Set_Time
	REM ECHO %STARTTIME%
	SET KEYFILE=%OUTPUTDIR%\%_label%_%SERVERID%_%STARTTIME%.txt
	
	IF DEFINED _VERBOSE (
		ECHO IPMITOOL -H %IPMISERVER% -U %IPMIUSER% -P %IPMIPWD% %_cmd% ^> "%KEYFILE%"
	) 

	IF EXIST "%KEYFILE%" GOTO :EOF
	IF DEFINED _TRY GOTO :exit_routine_1
	
	"%IPMITOOL%" -H %IPMISERVER% -U %IPMIUSER% -P %IPMIPWD% %_cmd% > "%KEYFILE%" 2>nul
	IF ERRORLEVEL 1 (
		IF DEFINED _NONEMPTY (
			GOTO :exit_routine_1
		)
	)

	IF DEFINED _VERBOSE (
		ECHO PYTHON %_label%.py "%KEYFILE%"
	)

	"%PYTHON%" %_label%.py "%KEYFILE%"

	IF ERRORLEVEL 1 GOTO :exit_routine_1
	
	IF NOT DEFINED _NODELETE (
		DEL "%KEYFILE%" >nul 2>nul
	)
	
:exit_routine_1
	IF NOT DEFINED NO_EXIT (
		EXIT
	)

	GOTO :EOF
	
:_sel_save_$time
	SET KEYFILE=%OUTPUTDIR%\sel_save_%SERVERID%_%STARTTIME%.txt
	IF DEFINED _VERBOSE (
		ECHO "%IPMITOOL%" -H %IPMISERVER% -U %IPMIUSER% -P %IPMIPWD% sel save "%KEYFILE%.save.txt" ^> "%KEYFILE%"
	)
	IF DEFINED _TRY GOTO :exit_routine_2
	
	IF EXIST "%KEYFILE%" GOTO :EOF

	"%IPMITOOL%" -H %IPMISERVER% -U %IPMIUSER% -P %IPMIPWD% sel save "%KEYFILE%.save.txt" > "%KEYFILE%" 2>nul
	IF ERRORLEVEL 1 (
		IF DEFINED _NONEMPTY (
			GOTO :exit_routine_2
		)
	)

	IF DEFINED _VERBOSE (
		ECHO PYTHON %_label%.py "%KEYFILE%"
	)
	
	"%PYTHON%" sel_save.py "%KEYFILE%"
	IF ERRORLEVEL 1 GOTO :exit_routine_2

	IF NOT DEFINED _NODELETE (
		DEL "%KEYFILE%" >nul 2>nul
		DEL "%KEYFILE%.save.txt" >nul 2>nul
	)
	
:exit_routine_2
	IF NOT DEFINED NO_EXIT (
		EXIT
	)

	GOTO :EOF
	
::arp               60    *
:arp
	SET subfun=%0
	SET subfun=%subfun:~1%
	SET KEYFILE=%OUTPUTDIR%\arp_%STARTTIME%.txt

	IF DEFINED _VERBOSE (
		ECHO "%ARPTOOL%" -a ^> "%KEYFILE%"
	)
	IF DEFINED _TRY GOTO :exit_routine_3
	
	IF EXIST "%KEYFILE%" GOTO :EOF
	
	"%ARPTOOL%" -a > "%KEYFILE%"
	REM ARP is always failed as expect as it always tries update with correct mac / ip
	REM IF ERRORLEVEL 1 (
	REM 	IF DEFINED _NONEMPTY (
	REM 		GOTO :EOF
	REM 	)
	REM )
	
	IF DEFINED _VERBOSE (
		ECHO PYTHON arp.py "%KEYFILE%"
	)
	
	"%PYTHON%" arp.py "%KEYFILE%"
	IF ERRORLEVEL 1 GOTO :exit_routine_3
	
	IF NOT DEFINED _NODELETE (
		DEL "%KEYFILE%" >nul 2>nul
	)
	
:exit_routine_3
	IF NOT DEFINED NO_EXIT (
		EXIT
	)

	GOTO :EOF
	
:ForEach_Server
	FOR /F "tokens=1,2,3,4" %%W IN (%SERVERLISTFILE%) DO (
		SET SERVERID=%%W
		SET IPMISERVER=%%X
		SET IPMIUSER=%%Y
		SET IPMIPWD=%%Z
		REM Check No Shift fields, that is, all 4 fields have value
		IF "!IPMIPWD!" NEQ "" (
			IF DEFINED SEQUENTIAL (
				CALL :Set_Time
				CALL :_%1
			) ELSE (
				IF DEFINED _VERBOSE (
					START /LOW "%1" cmd.exe /c %PROGRAM% _%1
				) ELSE (
					START /B /LOW "%1" cmd.exe /c %PROGRAM% _%1
				)
			)
		)
	)
	GOTO :EOF

:Set_Round_Time
	FOR /F %%T IN ('"%PYTHON%" Timestamp.py 0 %basetime% %cycletime%') DO (
		SET starttime=%%T
		SET starttime_slot=!starttime:~8,2!!starttime:~10,2!!starttime:~12,2!
	)
	GOTO :EOF

:Set_Round_Base_Time
	FOR /F %%T IN ('"%PYTHON%" Timestamp.py %1 %basetime% %cycletime%') DO (
		SET starttime=%%T
	)

	GOTO :EOF
	
:Set_Time
	FOR /F %%T IN ('"%PYTHON%" Timestamp.py') DO (
		SET starttime=%%T
	)
	GOTO :EOF

:Remove_Head
	SET isbody=
	SET Filename=%~1

	FOR /F "tokens=*" %%l in (%Filename%.bak) DO (
		IF NOT DEFINED isbody (
			SET isbody=1
		) ELSE (
			ECHO %%l>>"%Filename%.backup"
		)
	)
	COPY /Y "%Filename%.backup" "%Filename%" >nul 2>nul
	IF NOT DEFINED _NODELETE (
		DEL "%Filename%.bak" >nul 2>nul
		DEL "%Filename%.backup" >nul 2>nul
	)
	GOTO :EOF
	
:Exec_SQL
	IF DEFINED _VERBOSE (
		ECHO %MYSQL% -u%DBUSER% -p%DBPWD% -e "%~1"
	)
	"%MYSQL%" -u%DBUSER% -p%DBPWD% -e "%~1" > "%~2" 2>nul
	GOTO :EOF

:end
	POPD
	@ENDLOCAL
	
	REM @exit