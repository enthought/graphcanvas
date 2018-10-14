@ECHO OFF

SETLOCAL EnableDelayedExpansion

FOR /F "tokens=1,2 delims=." %%a in ("%EDM_VER%") do (
    SET MAJOR=%%a
    SET MINOR=%%b
)

SET EDM_MAJOR_MINOR=%MAJOR%.%MINOR%
SET EDM_PACKAGE=edm_%EDM_VER%_x86_64.msi
SET EDM_INSTALLER_PATH=C:\Users\travis\.cache\%EDM_PACKAGE%
SET COMMAND="(new-object net.webclient).DownloadFile('https://package-data.enthought.com/edm/win_x86_64/%EDM_MAJOR_MINOR%/%EDM_PACKAGE%', '%EDM_INSTALLER_PATH%')"

IF NOT EXIST %EDM_INSTALLER_PATH% CALL powershell.exe -Command %COMMAND% || GOTO error
CALL msiexec /qn /a %EDM_INSTALLER_PATH% TARGETDIR=c:\ || GOTO error

ENDLOCAL
@ECHO.DONE
EXIT

:error:
ENDLOCAL
@ECHO.ERROR
EXIT /b %ERRORLEVEL%
