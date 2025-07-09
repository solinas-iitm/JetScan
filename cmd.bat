@echo off

set Project_Drive=%~d0
set Apps_Path=%Project_Drive%\apps

%Project_Drive%
cd %~dp0

for %%I in (.) do set Project_Name=%%~nxI
set Home_Path=%cd%
cd "%Home_Path%"

REM
REM Add bin commands to path
REM

set Bin_Path=%Home_Path%\bin
set path="%Bin_Path%";%path%

REM
REM Add git folders to path
REM

set Git_Path=%Apps_Path%\Git
set Meld_Path=%Apps_Path%\Meld

set path="%Git_Path%";"%Meld_Path%";%path%

%windir%\system32\cmd.exe
