#!/usr/bin/python3
#
# Flashgun, by bufferbandit a.k.a claimittoyou
#
# A litle disclaimer...
# +--------------------------------------------------------+
# |This version of flashgun is not finished yet            |
# |This is just a beta, and there is a lot work to be done!|
# +--------------------------------------------------------+
# 
import glob , os , operator , platform , shutil , argparse
from urllib.parse import *
from lxml.html    import *
from requests     import *
from shutil       import *

OKBLUE = '\033[94m'
ENDC = '\033[0m'

def info( msg):
    print('\033[94m' + msg + '\033[0m')

def err( msg):
    print('\033[91m' + msg + '\033[0m')

def handle_arguments():
    arguments_used = False
    return arguments_used
    

def banner(off_on):
    if off_on:
        err("""
        +-----------------------------------------------------------------------------------------------+
        |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx| 
        |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx| 
        |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx+/:-.````|xxxxxxxxxxxxxxxxxxxxx| 
        |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx+:.``          |xxxxxxxxxxxxxxxxxxxxx| 
        |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx+-`              |xxxxxxxxxxxxxxxxxxxxx| 
        |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/.`              ` +xxxxxxxxxxxxxxxxxxxxx| 
        |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|                 `+xxxxxxxxxxxxxxxxxxxxxxx| 
        |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx-`               ``+xxxxxxxxxxxxxxxxxxxxxxxx| 
        |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx+`             `.:+++xxxxxxxxxxxxxxxxxxxxxxxxx| 
        |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|            `:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx| 
        |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx:`           `:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx| 
        |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx:            .+xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx| 
        |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/            .+xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx| 
        |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx+`           `+xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx| 
        |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`              xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx| 
        |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx-                       xxxxxxxxxxxxxxxxxxxxxxxxxxxx| 
        |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/                        xxxxxxxxxxxxxxxxxxxxxxxxxxxx| 
        |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx+`                        xxxxxxxxxxxxxxxxxxxxxxxxxxxx| 
        |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`                         xxxxxxxxxxxxxxxxxxxxxxxxxxxx| 
        |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.                          xxxxxxxxxxxxxxxxxxxxxxxxxxxx| 
        |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.            `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx| 
        |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx-            `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx| 
        |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx-            +xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx| 
        |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx-            `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx| 
        |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx+-             .xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx| 
        |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx-.              -xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx| 
        |xxxxxxxxxxxxxxxxxxxxxxxxx                    `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx| 
        |xxxxxxxxxxxxxxxxxxxxxxxx                   -xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx| 
        |xxxxxxxxxxxxxxxxxxxxxxxx               .-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx| 
        |xxxxxxxxxxxxxxxxxxxxxxxx            ../xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|
        |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|
        |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|
        |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx| 
        |xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx| 
        +-----------------------------------------------------------------------------------------------+
         
        """)
        print("          ________           __                      ")
        print("         / ____/ /___ ______/ /_  ____ ___  ______   ")
        print("        / /_  / / __ `/ ___/ __ \/ __ `/ / / / __ \  ")
        print("       / __/ / / /_/ (__  ) / / / /_/ / /_/ / / / /  ")
        print("      /_/   /_/\____/____/_/ /_/\__, /\____/_/ /_/   ")
        print("                                /___/                ")
        print("        SWF \n\n")
        print("        [Beta]")
    else:
        err("\t\t+-- Flashgun (+--+--+) SWF scanner --+")

def find_flare():
    if platform.system() == "Windows":
        flare_executable = "".join(glob.glob('*.exe'))
    else:
    #flare_executable = "".join(glob.glob('*.sh'))
        for x in os.listdir():
            inn = os.popen("file "+x).read()
        if "ELF" in inn:
            flare_executable = "./" + x

def create_dicts():
    for directory in ["log","buletin"]:
        if not os.path.exists(directory):
            os.makedirs(directory)

def check_empty():
    if os.listdir("buletin") != []:
        want_to_del = input(str(OKBLUE+"[?] Buletin isn't empty do you want to remove the files of the previous session [Y/n] "+ENDC))              
        yes = ["Yes","yes","y","Y",1]
        no = ["No","no","N","n",0]
        if want_to_del in yes: 
            for the_file in os.listdir("buletin"):
                file_path = os.path.join("buletin", the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                #elif os.path.isdir(file_path): shutil.rmtree(file_path)
                except Exception as e:
                    err("[!] Whoops, ther was an exception -->" + str(e))
        elif want_to_del in no:
            pass

        else:
            err("[+]Please enter one of these options.\n[+]Yes, Y, or 1 for yes\n[+]No, N or 0 for no\n")              
            exit()

    else:
        pass

def google_syntax(syntax_list):
    if type(syntax_list) is list:
        base_url = "https://www.google.nl/search?q="
        base_url += " ".join(syntax_list)
        base     += " "
        return base_url

    elif type(syntax_list) is str:
        base_url  = "https://www.google.nl/search?q="
        base_url += syntax_list
        base_url += " "
        return base_url

def google_search(input_url):
    base_url = google_syntax("ext:swf")
    urll = str(base_url  +
               input_url +
               "&filter=0").replace(",", " OR site:")
    
    raw   = get(urll).text 
    page  = fromstring(raw)
    return page
    
    

def google_get_urls(page):
    urls,swf_urls = [],[]

    for result in page.cssselect(".r a"):
        url = result.get("href")
        if url.startswith("/url?"):
            url = parse_qs(urlparse(url).query)['q']
        urls.append(url[0])
        swf_urls.append(url[0].partition('.swf')[0]+".swf")
   
    return swf_urls

def swf_url_download(swf_urls):
    if len(swf_urls) > 0:
        for urllist in swf_urls:
            info("[+] Url  containing swf file found: " + urllist)
            filename = "buletin/"+urlsplit(urllist).path.split("/")[-1]
            try:
                response = get(urllist)
            except:
                err("[+] Whoops something wrong with the requst to "+urllist)
                continue
            if response.ok:
                try:
                    file = open(filename, "wb+") 
                    file.write(response.content)
                    file.close()
                    info("[+] File " +  filename.replace("buletin/","") + " detected and written to the disk")
                    info("[+] File "+ filename.replace("buletin/","")+ " decompiled with flare " + os.popen(flare_executable + " " + filename))
                except:
                    pass
                          
            else:
                err("[!] Failed to get "+filename.replace("buletin/","")+ " at url "+ urllist)
                swf_urls.remove(urllist)
                
                        
    else:
        err("[!] No urls containing swf files found :(")

# This function (decompile_swf_files) should be re-written.
# There should be a zip file with all the versions of flare
# packed as flare_files.zip
#           |
#           +-flare_Windows.exe
#           +-flare_Linux32bit
#           +-flare_Linux64bit
#
# than the function should only unzip file = "flare_" +platform.system()
# and put this file intoto the flare_executable variable.
# At tge moment I only have a windows executable but by modifying
# the flare_executable variable you can use your own flare version
# available at http://www.nowrap.de/flare.html
#
# Flare version table
# +-------------------------------------------------------------------------+
# | Windows         --> http://www.nowrap.de/download/flare06doswin.zip     |
# | OSX             --> http://www.nowrap.de/download/flare06mac.tgz        |
# | Linux x86       --> http://www.nowrap.de/download/flare06linux.tgz      |
# | Linux x86 64bit --> http://www.nowrap.de/download/flare06linux64.tgz    |
# | Solaris x86     --> http://www.nowrap.de/download/flare06solaris.tgz    |
# +-------------------------------------------------------------------------+
    
def decompile_swf_files(dirextionary="buletin"):
    if platform.system() == "Windows":
        appendix = ".exe"
    else:
        appendix = ""
    flare_executable =  "flare_" +platform.system() + appendix
    flash_dir = dirextionary
    os.chdir("buletin")
    flares = {}
    flare_files_in_buletin = glob.glob("*.flr")
    if len(flare_files_in_buletin) > 0:
        for flare_file in flare_files_in_buletin:
            flares.update(
            {
            flare_file.replace(".flr",""):open(flare_file,'r', encoding="utf8").read()
            })
    else:
        err("[!] No flare files found")

   
    
    return flares

def get_positions(list_to_search_in,word_to_find):

    effected_dangerous_function_positions = []
    if word_to_find in list_to_search_in:
       for i, j in enumerate(list_to_search_in):
            if j == word_to_find:

                effected_dangerous_function_positions.append(i)
    return effected_dangerous_function_positions

def anything(iterable):
    for element in iterable:
        if element:
            global effected_items
            effected_items = list(iterable)
            return True
    return False

# This function (scan_functions) does not work yet.
# Just having some problems with porting it into a function
# Shouldn't have too much problem with fixing this so this will be
# fixed in the next version

def scan_functions():
    flares = decompile_swf_files()
    for file_containing_dangerous_function, swf_source_code in flares.items():
        if anything(n in swf_source_code for n in dangerous_functions):
            positions = get_positions(effected_items,True)
            for x in positions:
                vuln_functions = []
                for y in positions:
                    err("[+] A dangerous function found in file: " + file_containing_dangerous_function+"--> "+operator.itemgetter(y)(dangerous_functions))

# Also in the next version there will be a totally new function that
# will upload the SWF files to cure53 flashbang (at https://cure53.de/flashbang)
# or at your own host if you want to (project is available at https://github.com/cure53/Flashbang/)
# a tool that extracts flashvars and returns a url with parameters.
# Than it will bruteforce all
# parameters with a list of payloads. Maybe there will be a mechanism checking
# if the payload has been executed but scince we're working with flash
# we can't just look into the page source and see if the payload is refelcted so
# that might be a problem.
# Also I should "repaint" some dialogs with different colors.


def __main__():
    if not handle_arguments():
        find_flare()
        create_dicts()
        banner(1)
        check_empty()
        input_url = input(
                   "                                          "
                  +"[i] Enter the site you want to crawl.   \n"
                  +"[i] Since this is the google search       "
                  +"engine you can use the google syntax    \n" 
                  +"[i] Enter '*.site' for all subdomains.  \n"
                  +"[i] Enter both to do both, have fun :)  \n"
                  +"[i] Enter '*.site.*' for all tld's      \n"
                  +"[i] Enter -something to exclude           "
                  +"something (e.g a subdomain or tld)      \n"
                  +"[i] Use the 'OR' command to scan multiple sites "
                  +"(e.g target1 OR site:target2)           \n"
                  +"[i] Or separate them by a comma         \n"
                  +"[+] Have fun :)                         \n"
                  +"[?] Website:                              
                  )
        page  = google_search(input_url)
        swf_urls = google_get_urls(page)
        swf_url_download(swf_urls)
        #decompile_swf_files() ~todo
        #scan_functions()      ~todo
        
    else:
        # The last thing that's on the todo list is implementing 
        # a headless version that just checks if there are
        # any arguments and replaces variables like input_url with
        # command line arguments
        pass

if __name__ == "__main__":
    __main__()
        

    
