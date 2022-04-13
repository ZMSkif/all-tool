@echo off
setlocal enableextensions enabledelayedexpansion
@echo Hi User
set /P base="Send base here. ->  "

FINDSTR /L "@yandex.ru" %base% > yandex.ru.txt
FINDSTR /L "@yandex.org" %base% > yandex.org.txt
FINDSTR /L "@yandex.net" %base% > yandex.net.txt
FINDSTR /L "@yandex.net.ru" %base% > yandex.net.ru.txt
FINDSTR /L "@yandex.com.ru" %base% > yandex.com.ru.txt
FINDSTR /L "@yandex.ua" %base% > yandex.ua.txt
FINDSTR /L "@yandex.com.ua" %base% > yandex.com.ua.txt
FINDSTR /L "@yandex.by" %base% > yandex.by.txt
FINDSTR /L "@yandex.eu" %base% > yandex.eu.txt
FINDSTR /L "@yandex.ee" %base% > yandex.ee.txt
FINDSTR /L "@yandex.lt" %base% > yandex.lt.txt
FINDSTR /L "@yandex.lv" %base% > yandex.lv.txt
FINDSTR /L "@yandex.md" %base% > yandex.md.txt
FINDSTR /L "@yandex.uz" %base% > yandex.uz.txt
FINDSTR /L "@yandex.mx" %base% > yandex.mx.txt
FINDSTR /L "@yandex.do" %base% > yandex.do.txt
FINDSTR /L "@yandex.tm" %base% > yandex.tm.txt
FINDSTR /L "@yandex.de" %base% > yandex.de.txt
FINDSTR /L "@yandex.ie" %base% > yandex.ie.txt
FINDSTR /L "@yandex.in" %base% > yandex.in.txt
FINDSTR /L "@yandex.qa" %base% > yandex.qa.txt
FINDSTR /L "@yandex.so" %base% > yandex.so.txt
FINDSTR /L "@yandex.nu" %base% > yandex.nu.txt
FINDSTR /L "@yandex.tj" %base% > yandex.tj.txt
FINDSTR /L "@yandex.dk" %base% > yandex.dk.txt
FINDSTR /L "@yandex.es" %base% > yandex.es.txt
FINDSTR /L "@yandex.pt" %base% > yandex.pt.txt
FINDSTR /L "@yandex.pl" %base% > yandex.pl.txt
FINDSTR /L "@yandex.lu" %base% > yandex.lu.txt
FINDSTR /L "@yandex.it" %base% > yandex.it.txt
FINDSTR /L "@yandex.az" %base% > yandex.az.txt
FINDSTR /L "@yandex.ro" %base% > yandex.ro.txt
FINDSTR /L "@yandex.rs" %base% > yandex.rs.txt
FINDSTR /L "@yandex.sk" %base% > yandex.sk.txt
FINDSTR /L "@yandex.no" %base% > yandex.no.txt
FINDSTR /L "@ya.ru" %base% > ya.ru.txt
FINDSTR /L "@yandex.com" %base% > yandex.com.txt
FINDSTR /L "@yandex.asia" %base% > yandex.asia.txt
FINDSTR /L "@yandex.mobi" %base% > yandex.mobi.txt
FINDSTR /L "@mail.ru" %base% > mail.ru.txt
FINDSTR /L "@internet.ru" %base% > internet.ru.txt
FINDSTR /L "@list.ru" %base% > list.ru.txt
FINDSTR /L "@bk.ru" %base% > bk.ru.txt
FINDSTR /L "@inbox.ru" %base% > inbox.ru.txt
FINDSTR /L "@mail.ua" %base% > mail.ua.txt
FINDSTR /L "@ukr.net" %base% > ukr.net.txt
FINDSTR /L "@rambler.ru" %base% > rambler.ru.txt
FINDSTR /L "@lenta.ru" %base% > lenta.ru.txt
FINDSTR /L "@autorambler.ru" %base% > autorambler.ru.txt
FINDSTR /L "myrambler.ru" %base% > myrambler.ru.txt
FINDSTR /L "@ro.ru" %base% > ro.ru.txt
FINDSTR /L "@rambler.ua" %base% > rambler.ua.txt
FINDSTR /L "@gmail.com" %base% > gmail.com.txt
copy /b yandex.ru.txt + yandex.org.txt + yandex.net.txt + yandex.net.ru.txt + yandex.com.ru.txt + yandex.ua.txt + yandex.com.ua.txt + yandex.by.txt + yandex.eu.txt + yandex.ee.txt + yandex.lt.txt + yandex.lv.txt + yandex.md.txt + yandex.uz.txt + yandex.mx.txt + yandex.do.txt + yandex.tm.txt + yandex.de.txt + yandex.ie.txt + yandex.in.txt + yandex.qa.txt + yandex.so.txt + yandex.nu.txt + yandex.tj.txt + yandex.dk.txt + yandex.es.txt + yandex.pt.txt + yandex.pl.txt + yandex.lu.txt + yandex.it.txt + yandex.az.txt + yandex.ro.txt + yandex.rs.txt + yandex.sk.txt + yandex.no.txt + ya.ru.txt + yandex.com.txt + yandex.asia.txt + yandex.mobi.txt + mail.ru.txt + internet.ru.txt + list.ru.txt + bk.ru.txt + inbox.ru.txt + mail.ua.txt + ukr.net.txt + rambler.ru.txt + lenta.ru.txt + autorambler.ru.txt + myrambler.ru.txt + ro.ru.txt + rambler.ua.txt + gmail.com.txt %base%-MYR.txt
del /q yandex.ru.txt yandex.org.txt yandex.net.txt yandex.net.ru.txt yandex.com.ru.txt yandex.ua.txt yandex.com.ua.txt yandex.by.txt yandex.eu.txt yandex.ee.txt yandex.lt.txt yandex.lv.txt yandex.md.txt yandex.uz.txt yandex.mx.txt yandex.do.txt yandex.tm.txt yandex.de.txt yandex.ie.txt yandex.in.txt yandex.qa.txt yandex.so.txt yandex.nu.txt yandex.tj.txt yandex.dk.txt yandex.es.txt yandex.pt.txt yandex.pl.txt yandex.lu.txt yandex.it.txt yandex.az.txt yandex.ro.txt yandex.rs.txt yandex.sk.txt yandex.no.txt ya.ru.txt yandex.com.txt yandex.asia.txt yandex.mobi.txt mail.ru.txt internet.ru.txt list.ru.txt bk.ru.txt inbox.ru.txt mail.ua.txt ukr.net.txt rambler.ru.txt lenta.ru.txt autorambler.ru.txt myrambler.ru.txt ro.ru.txt rambler.ua.txt gmail.com.txt
echo "fuckoff zabugor"

@del /q temp.txt
cls
echo ZMS