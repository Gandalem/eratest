@echo off
where git >nul 2>&1
if %errorlevel%==0 (
    SET "GOT_GIT=true"
rem      goto :eof
)
where tar >nul 2>&1
if %errorlevel%==0 (
    SET "GOT_TAR=true"
rem      goto :eof
)

if "%GOT_GIT%"=="" (
    CLS
    if "%GOT_TAR%"=="" (
        CLS
        echo -------------------------------------------------------------------
        echo Git and Tar not found...
        echo Please install Git for Windows and Tar for Windows before proceeding.
        echo -------------------------------------------------------------------
        echo Git: https://github.com/git-for-windows/git/releases
        echo Tar: https://gnuwin32.sourceforge.net/packages/gtar.htm
        echo -------------------------------------------------------------------
        echo If you are on Linux, please use [- 2 Launch TW.sh] instead
        echo -------------------------------------------------------------------
rem          START https://github.com/git-for-windows/git/releases
        pause
        exit
    ) else (
        CLS
        echo -------------------------------------------------------------------
        echo Git not found...
        echo Please install Git for Windows before proceeding.
        echo -------------------------------------------------------------------
        echo If you are on Linux, please use [- 2 Launch TW.sh] instead
        echo -------------------------------------------------------------------
        START https://github.com/git-for-windows/git/releases
        pause
        exit
    )
) else if "%GOT_TAR%"=="" (
    CLS
    echo -------------------------------------------------------------------
    echo Tar not found...
    echo Please install Tar for Windows before proceeding.
    echo -------------------------------------------------------------------
    echo If you are on Linux, please use [- 2 Launch TW.sh] instead
    echo -------------------------------------------------------------------
    START https://gnuwin32.sourceforge.net/packages/gtar.htm
    pause
    exit
) else if NOT EXIST id_ed25519_eraCorrectionHub (
    echo -------------------------------------------------------------------
	echo id_ed25519_eraCorrectionHub file not found...
	echo This file is used to authenticate with the host server and is required to use this launcher.
	echo Please re-extract eraNAS.
    echo -------------------------------------------------------------------
	pause
	exit
)


SET GIT_SSH_COMMAND=ssh -i id_ed25519_eraCorrectionHub

echo ---- Downloading VERSION file ----

rem ---- This no longer works cause cloudflare, using git archive instead, meh, didn't work on proton anyway.
echo If it asks for you credentials just don't enter anything, if it asks you abut SSH keys respond with yes.

git archive --remote=git@ssh.gitgud.io:mrpopsalot/pops-tw "dev/omogatari-kai" VERSION | tar -xO > VERSION
rem  powershell -Command "(New-Object Net.WebClient).DownloadFile('%URLBASE%/%BRANCH%/%FILE%', '%FILE%')"
rem powershell -Command "Invoke-WebRequest %URLBASE%/%BRANCH%/%FILE% -OutFile %FILE%"
rem  pause
echo Launching eraNAS. Have fun!
C:\Windows\System32\cmd.exe /c start "TW" /affinity 3 "LazyLoadingV26.exe"
wmic process where name="LazyLoadingV26.exe" CALL setpriority 128
