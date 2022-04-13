import os, requests, argparse, colorama, ScrapeSearchEngine, time, threading
from colorama import Fore, Back
from ScrapeSearchEngine.SearchEngine import *

class Settings():
    def __init__(self):
        pass

    def clear(self):
        os.system('cls' if os.name == "nt" else 'clear')

    def banner(self):
        print(Fore.YELLOW+f"""
        ___
       __H__     {Back.RED}{Fore.RESET}Made By Kaneki Web{Fore.YELLOW}{Back.RESET}
 ___ ___[{Back.RED}){Back.RESET}]___ ___ ___ ___ ___ ___ ___ 
|_ -| . [{Back.RED}({Back.RESET}]_ -|  _| .'|   |   | -_|  _|
|___|_  [{Back.RED},{Back.RESET}]___|___|__,|_|_|_|_|___|_|  
      |_|V...                              

"""+Fore.RESET)

def scanner(link):
	Found = False
	try:
		error_list = [
		    # MySQL
		    "you have an error in your sql syntax;",
		    "warning: mysql",
		    "mysql",
		    # SQL Server
		    "unclosed quotation mark after the character string",
		    # Oracle
		    "quoted string not properly terminated",

		    "mysql_fetch",
		    "Error Executing Database Query",
		    "Microsoft OLE DB Provider for SQL Server",
		    "SQLServer JDBC Driver",
		    "Unclosed quotation mark",
		    "ODBC Microsoft Access Driver",
		    "Microsoft JET Database",
		    "Error Occurred While Processing Request",
		    "Microsoft OLE DB Provider for ODBC Drivers error",
		    "mysql_fetch_array()",
		    "Syntax error",
		    "mysql_numrows()",
		    "GetArray()",
		    "FetchRow()"
		]

		r = requests.get(f"{link}'").text.lower()

		for error in error_list:
		    if error in r:
		    	if Found == False:
		    		Found = True
		    		open('vuln.txt', 'a+').write(link+"\n")
		    		print(f"[{Fore.CYAN}{time.strftime('%H:%M:%S')}{Fore.RESET}] [{Fore.GREEN}VULN{Fore.RESET}] "+link)
	
	except:
		print(f"[{Fore.CYAN}{time.strftime('%H:%M:%S')}{Fore.RESET}] [{Fore.RED}ERROR{Fore.RESET}] Connection Error !")


Settings().clear()
Settings().banner()

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dorks", help="Your dorks list", required=True)
parser.add_argument("-s", "--scan", help="Enable scanner ex: -s true/false")
parser.add_argument("-e", "--engine", help="Search engine ex: google, yahoo, bing...")
args = parser.parse_args()

with open(args.dorks, 'r') as f:
    dorks = [line.strip('\n') for line in f]

scraped = 0
for dork in dorks:
    if os.name == "nt":
        os.system('title SQLI Crawler ^| Dork: '+str(dork)+' ^| Scraped Links: '+str(scraped))

    try:
        search = (dork)        
        if args.engine.lower() == "bing":
            bingText, bingLink = Bing(search=search, userAgent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.96 Safari/537.36")
            ScrapedLinks = bingLink[0:10]
        
        elif args.engine.lower() == "yahoo":
            yahooText, yahooLink = Yahoo(search=search, userAgent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.96 Safari/537.36")
            ScrapedLinks = yahooLink[0:10]
        
        elif args.engine.lower() == "google":
            googleText, googleLink = Google(search=search, userAgent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.96 Safari/537.36")
            ScrapedLinks = googleLink[0:10]
        
        elif args.engine.lower() == "duckduckgo":
            duckduckgoText, duckduckgoLink = Duckduckgo(search=search, userAgent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.96 Safari/537.36")
            ScrapedLinks = duckduckgoLink[0:10]
        
        elif args.engine.lower() == "givewater":
            givewaterText, givewaterLink = Givewater(search=search, userAgent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.96 Safari/537.36")
            ScrapedLinks = givewaterLink[0:10]
        
        elif args.engine.lower() == "ask":
            askText, askLink = Ask(search=search, userAgent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.96 Safari/537.36")
            ScrapedLinks = askLink[0:10]
        
        else:
            bingText, bingLink = Bing(search=search, userAgent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.96 Safari/537.36")
            ScrapedLinks = bingLink[0:10]

        for link in ScrapedLinks:
            scraped += 1
            open('links.txt', 'a+').write(link+"\n")

            print(f"[{Fore.CYAN}{time.strftime('%H:%M:%S')}{Fore.RESET}] [{Fore.YELLOW}INFO{Fore.RESET}] "+link)

            if args.scan == 'true':
                threading.Thread(target=scanner, args=(link, )).start()

    except Exception as e:
        print(e)
        exit()
