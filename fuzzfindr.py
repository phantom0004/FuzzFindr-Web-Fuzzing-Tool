# Example URLS for testing ethically: http://testphp.vulnweb.com  or  http://www.itsecgames.com
# ---------------------------------------------------------------------------------------
# This program, created by Phantom, is intended for ethical and responsible security
# testing only. Use it exclusively on systems where you have explicit authorization.
# Unauthorized use of this software is illegal and unethical.
# ---------------------------------------------------------------------------------------
import requests
from termcolor import colored
from bs4 import BeautifulSoup, Comment
import time
import sys
import uuid

def display_banner():
    banner = """
    $$$$$$$$\                            $$$$$$$$\ $$\                 $$\           
    $$  _____|                           $$  _____|\__|                $$ |          
    $$ |   $$\   $$\ $$$$$$$$\ $$$$$$$$\ $$ |      $$\ $$$$$$$\   $$$$$$$ | $$$$$$\  
    $$$$$\ $$ |  $$ |\____$$  |\____$$  |$$$$$\    $$ |$$  __$$\ $$  __$$ |$$  __$$\ 
    $$  __|$$ |  $$ |  $$$$ _/   $$$$ _/ $$  __|   $$ |$$ |  $$ |$$ /  $$ |$$ |  \__|
    $$ |   $$ |  $$ | $$  _/    $$  _/   $$ |      $$ |$$ |  $$ |$$ |  $$ |$$ |      
    $$ |   \$$$$$$  |$$$$$$$$\ $$$$$$$$\ $$ |      $$ |$$ |  $$ |\$$$$$$$ |$$ |      
    \__|    \______/ \________|\________|\__|      \__|\__|  \__| \_______|\__|                                                                                 
    """
    banner_msg = colored("Your Ultimate Fuzzing Companion <3", 'red')
    print(banner+banner_msg+"\t\tUnauthorised usage is prohibited")
    print("\n") # Reduce clutter
    
def start_fuzzer(wordlist_path, website_link, verbose="N", delay=0.3, write_to_file=False):
    global log_file, redirect_counter
    with open(wordlist_path, "r") as wordlist:
        for word in wordlist: 
            time.sleep(delay) # Prevent "too many requests" status code or else even a potential website block  
            word = word.strip()
            try:
                res = requests.get(url=f"{website_link}/{word}", allow_redirects=False)
                check_for_redirects(res.status_code, redirect_counter)
            except KeyboardInterrupt:
                break
            except TimeoutError:
                print("Connection timeout, trying another word . . .")
                continue
            
            if res.status_code == 404: continue
            
            print("[!] DIRECTORY FOUND : " + colored(word, "green") + f"    [Full Link : {website_link}/{word}]")
            if write_to_file == True: log_to_file(f"[!] DIRECTORY FOUND : {word} [Full Link : {website_link}/{word}] \n", log_file)
                
            if verbose == "Y":
                try:
                    html_extract = BeautifulSoup(res.content, "html.parser") # Extract HTML code from website
                except:
                    print(colored(f"[-] Unable to extract HTML from website [Status Code Retrieved : {res.status_code}]", "red"))
                    if write_to_file == True: log_to_file(f"[-] Unable to extract HTML from website [Status Code Retrieved : {res.status_code}] \n", log_file)
                    print("\n") # Reduce below clutter
                    continue
                finally:
                    error_check(res.status_code) # Check if the website entered returns any error
                
                stored_links, stored_titles, stored_comments, stored_forms = (verbose_output(html_extract))
                for links in stored_links:
                    if links is None:
                        pass
                    if write_to_file == True: log_to_file(f"[+] FOUND LINK : {links} \n", log_file)
                    else:
                        print(f"[+] FOUND LINK : {links}")
                
                for titles in stored_titles:
                    if titles is None:
                        pass
                    if write_to_file == True: log_to_file(f"[+] FOUND TITLE : {titles} \n", log_file)
                    else:
                        print(f"[+] FOUND TITLE : {titles}")
                    
                for comments in stored_comments:
                    if comments is None:
                        pass
                    if write_to_file == True: log_to_file(f"[+] FOUND COMMENT : {comments} \n", log_file)
                    else:
                        print(f"[+] FOUND COMMENT : {comments}")
                    
                for forms in stored_forms:
                    if forms is None:
                        pass
                    if write_to_file == True: log_to_file(f"[+] FOUND FORM : {forms} \n", log_file)
                    else:
                        print(f"[+] FOUND FORM : {forms}")
                    
                print("\n") # Reduce below clutter
                if write_to_file == True: log_to_file("\n", log_file)
    
def verbose_output(html_content):
    links, titles, comments, forms = [], [], [], []
    
    for link in html_content.find_all("a"):
        try:
            links.append(link.string)
        except:
            links.append("Error encountered, RAW OUTPUT - "+str(links))
        
    for title in html_content.find_all("title"):
        try:
            titles.append(title.string)
        except:
            titles.append("Error encountered, RAW OUTPUT - "+str(title))
    
    for comment in html_content.find_all(string=lambda text: isinstance(text, Comment)):
        try:
            comments.append(comment[:60])
        except:
            comments.append("Error encountered, RAW OUTPUT - "+str(comment))
    
    for form in html_content.find_all("form"):
        try:
            action = form.get('action')
            if action:
                forms.append(action)
        except:
            forms.append("Error encountered, RAW OUTPUT - "+str(form))
        
    return links, titles, comments, forms

def error_check(response):
    website_error_messages = {
        403: "Server understood the request but refuses to authorize it [Forbidden]",
        408: "The server timed out waiting for the request [Request Timeout]",
        429: "Too many requests have been sent in a given amount of time [Too Many Requests]",
        500: "Server encountered an unexpected condition [Internal Server Error]",
        502: "Received an invalid response from the upstream server [Bad Gateway]",
        503: "Server is temporarily overloaded or down for maintenance [Service Unavailable]",
        504: "Did not receive a timely response from the upstream server [Gateway Timeout]"
    }

    if response in website_error_messages:
        print(f"[!] More info : {website_error_messages[response]}")

def handle_user_arguments():        
    if len(sys.argv) != 3:
        return None, None
    
    try:
        website_link = sys.argv[1]
        wordlist_path = sys.argv[2]
        
        return website_link, wordlist_path
    except:
        return None, None

def fetch_time():
    current_time = time.localtime()
    formatted_time = time.strftime("%H:%M:%S", current_time)
    return formatted_time

def log_to_file(content, file_name):
    with open(file_name, "a") as log_file:
        log_file.write(content)

def check_for_redirects(status_code, redirections_happened):    
    if status_code in range(300,399):
        print("[!] Website redirection detected! Pausing before next redirect . . .")
        redirections_happened[0] += 1
        
        if redirections_happened[0] < 3:
            time.sleep(2.5) # Add small delay
        else:
            time.sleep(5) # Add large delay
    else:
        redirections_happened[0] = 0
    
    if redirections_happened[0] == 6:
        exit("Server keeps redirecting, this is possibly due to the fact that it has noticed the fuzzing attempts")

display_banner()

website_link, wordlist_path = handle_user_arguments()
verbose_log_flag = False
log_file = None
redirect_counter = [0] # Mimics a 'static' datatype

if website_link is None or wordlist_path is None:
    exit("[-] Incorrect usage detected. Please run the program as follows:\n"
     "    python3 fuzzfindr.py <website_link> <wordlist_path>\n"
     "Example:\n"
     "    python3 fuzzfindr.py http://vulnerablewebsite.com fuzz_wordlist.txt")

if website_link[-1:] == "/":
    website_link = website_link[:-1]

try:
    if (file := open(wordlist_path, "r")): file.close()
except FileNotFoundError:
    exit("[-] Wordlist cannot be found, ensure directory is valid")
except OSError:
    exit("[-] Incorrect format for wordlist text file, ensure path and file name is valid")

verbose_option = input("The verbose option displays HTML content on the screen. Enable verbose option? [Y/N] (Default is 'N'): ").upper()
if verbose_option == "Y":
    print(colored("[!] Verbose option is slower as it will return a detailed output [displays links, titles, comments and forms]\n", 'yellow', attrs=['bold']))
    
    verbose_log_option = input("Do you want to log verbose output silently to a file? [Y/N] (Default is 'N'): ").upper()
    if verbose_log_option == "Y":
        print(colored("[!] Verbose option set to True. Verbose logs will not be shown in terminal but saved in a text file\n", 'yellow', attrs=['bold']))
        verbose_log_flag = True
        log_file = "fuzzfindr_log-"+str(uuid.uuid4())[:8] + ".txt"

try:
    delay_option = float(input("Enter a delay option in between requests (Default is 0.3 seconds): "))
    if delay_option < 0: 
        print("[-] Unable to handle negative delays, defaulting to 0.3 seconds")
        delay_option = 0.3
except:
    print("[-] Invalid float value entered, defaulting to 0.3 seconds")

print(colored(f"[!] Started Fuzzing at : {fetch_time()} [Press ctrl+c to abort]\n", 'yellow', attrs=['bold']))
start_fuzzer(wordlist_path, website_link, verbose_option, delay_option, verbose_log_flag)

print(colored(f"[!] Fuzzing ended at : {fetch_time()}\n", 'yellow', attrs=['bold']))
if log_file is not None:
    print(colored(f"[+] Verbose log file saved at : {log_file}", 'green'))
