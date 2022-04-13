@echo off
set /P base="Enter base filename with extension! (eg. MyBase.txt) ->  "
find /c /v "" <"%base%"
pause