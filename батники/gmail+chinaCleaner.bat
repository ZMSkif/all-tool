@echo off
color 37 
setlocal enableextensions enabledelayedexpansion
@echo Hi, BHF. made by meatboy
set /P base="ведите имя базы или перетащите ее в это окно. ->  "

FINDSTR /L "@hanmail.net" %base% > hanmail.txt
FINDSTR /L "@daum.net" %base% > daum.txt
FINDSTR /L "@21cn.com" %base% > 21cn.txt
FINDSTR /L "@126.com" %base% > 126.txt
FINDSTR /L "@qq.com" %base% > qqcom.txt
FINDSTR /L "@gmail.com" %base% > %base%-gmail.txt
copy /b hanmail.txt + temp.txt + daum.txt + temp.txt + 21cn.txt + temp.txt + 126.txt + temp.txt + qqcom.txt %base%-cnine.txt
del /q hanmail.txt  daum.txt  21cn.txt  126.txt  qqcom.txt
echo "fuckoff china"

FINDSTR /L /v /I "@hanmail.net @daum.net @21cn.com @126.com @qq.com @gmail.com" %base% > %base%-Clean.txt
@del /q temp.txt
cls
echo "*(*(*-*)*)*"