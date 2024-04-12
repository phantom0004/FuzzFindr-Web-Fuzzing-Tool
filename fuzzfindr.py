# Example URLS for testing ethically: http://testphp.vulnweb.com  or  http://www.itsecgames.com
# ---------------------------------------------------------------------------------------
# This program, created by Phantom, is intended for ethical and responsible security
# testing only. Use it exclusively on systems where you have explicit authorization.
# Unauthorized use of this software is illegal and unethical.
# ---------------------------------------------------------------------------------------
# Check me out on GitHub! -> https://github.com/phantom0004
#---------------------------------------------------------------------------------------
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
    
def start_fuzzer(wordlist_path, website_link, delay, verbose="N", write_to_file=False):
    global log_file, redirect_counter
    with open(wordlist_path, "r") as wordlist:
        for word in wordlist: 
            try:
                time.sleep(float(delay)) # Prevent "too many requests" status code or else even a potential website block 
            except KeyboardInterrupt:
                break 
            word = word.strip()
            try:
                res = requests.get(url=f"{website_link}/{word}", allow_redirects=False)
                check_for_redirects(res.status_code, redirect_counter)
            except KeyboardInterrupt:
                break
            except TimeoutError:
                print("Connection timeout, skipping . . .")
                continue
            except requests.RequestException as res_error:
                print(f"[-] An exception occured within the requests library - {res_error}")
                break
            
            if res.status_code == 404: continue
            
            if verbose == "Y":
                print("[+] DIRECTORY FOUND : " + colored(word, "green") + f"    [Full Link : {website_link}/{word}]")
            else:
                print("[+] DIRECTORY FOUND : " + colored(word, "green") + f"    [Full Link : {website_link}/{word}] \n")
                
            if write_to_file == True: log_to_file(f"[+] DIRECTORY FOUND : {word} [Full Link : {website_link}/{word}] \n", log_file)
                
            if verbose == "Y":
                try:
                    if res.content and 'text/html' in res.headers.get('Content-Type', ''):
                        html_extract = BeautifulSoup(res.content, "html.parser") # Extract HTML code from website
                    else:
                        print(colored("[-] Non-HTML content received or empty response, skipping parsing \n", "red"))
                        if write_to_file == True: log_to_file("[-] Non-HTML content received or empty response, skipping parsing \n", log_file)
                        continue
                except:
                    if write_to_file == True: 
                        log_to_file(f"[-] Unable to extract HTML from website [Status Code Retrieved : {res.status_code}] \n", log_file)
                    else:
                        print(colored(f"[-] Unable to extract HTML from website [Status Code Retrieved : {res.status_code}] \n", "red"))
                    continue
                finally:
                    error_check(res.status_code) # Check if the website returned any error
                
                stored_links, stored_titles, stored_comments, stored_forms = (verbose_output(html_extract))
                if stored_links is None and stored_titles is None and stored_comments is None and stored_forms is None:
                    print(colored("[-] No data was able to be extracted for this section \n", "red"))
                    continue # Skip below code as no data is stored
                    
                for links in stored_links:
                    if links is None: pass
                    
                    if write_to_file == True: 
                        log_to_file(f"   --> [+] FOUND LINK : {links} \n", log_file)
                    else:
                        print(f"   --> [+] FOUND LINK : {colored(links, 'green')}")
                
                for titles in stored_titles:
                    if titles is None: pass
                    
                    if write_to_file == True: 
                        log_to_file(f"   --> [+] FOUND TITLE : {titles} \n", log_file)
                    else:
                        print(f"   --> [+] FOUND TITLE : {colored(titles, 'green')}")
                    
                for comments in stored_comments:
                    if comments is None: pass
                    
                    if write_to_file == True: 
                        log_to_file(f"   --> [+] FOUND COMMENT : {comments} \n", log_file)
                    else:
                        print(f"   --> [+] FOUND COMMENT : {colored(comments, 'green')}")
                    
                for forms in stored_forms:
                    if forms is None: pass
                    
                    if write_to_file == True: 
                        log_to_file(f"   --> [+] FOUND FORM : {forms} \n", log_file)
                    else:
                        print(f"   --> [+] FOUND FORM : {colored(forms, 'green')}")
                
                # Reduce clutter    
                if write_to_file == True: log_to_file("\n", log_file) 
                else: print("\n")
    
def verbose_output(html_content):
    links, titles, comments, forms = [], [], [], []
    
    for link in html_content.find_all("a"):
        try:
            href = link.get('href') # Different logic for links as stripping normally doesnt work always
            if href:
                links.append(href.strip())
        except AttributeError:
            links.append("Error encountered, RAW OUTPUT - "+str(links))
        
    for title in html_content.find_all("title"):
        try:
            if title.string:
                titles.append(title.string.strip())
        except AttributeError:
            titles.append("Error encountered, RAW OUTPUT - "+str(title))
    
    for comment in html_content.find_all(string=lambda text: isinstance(text, Comment)):        
        try:
            if comment:
                comments.append(comment.strip()[:60])
        except AttributeError:
            comments.append("Error encountered, RAW OUTPUT - "+str(comment))
    
    for form in html_content.find_all("form"):        
        try:
            action = form.get('action')
            if action:
                forms.append(action.strip())
        except AttributeError:
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
    exit("[-] Incorrect usage detected. Please run the program as follows: python3 fuzzfindr.py <website_link> <wordlist_path>\n"
     "Example: python3 fuzzfindr.py http://vulnerablewebsite.com fuzz_wordlist.txt\n\n"
     "For more information, check: https://github.com/phantom0004/FuzzFindr-Web-Fuzzing-Tool")

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
        log_file = "fuzzfindr_log-"+str(uuid.uuid4())[:6] + ".txt"
    else:
        print(colored(f"[!] Verbose output will be displayed on terminal only\n", 'yellow', attrs=['bold']))

try:
    delay_option = float(input("Enter a delay option in between requests (Default is no delay!): "))
    if delay_option < 0: 
        delay_option = 0
except:
    delay_option = 0
finally:
    print(colored(f"[!] Delay option set to {delay_option} seconds\n", 'yellow', attrs=['bold']))

print(colored(f"[!] Started Fuzzing at : {fetch_time()} [Press ctrl+c to abort]", attrs=['bold']))
start_fuzzer(wordlist_path, website_link, delay_option, verbose_option, verbose_log_flag)

print(colored(f"[!] Fuzzing ended at : {fetch_time()}", attrs=['bold']))
if log_file is not None:
    print(colored(f"[+] Verbose log file saved at : {log_file} (Stored same directory as fuzzfindr)", 'green'))
    
print("\nThe fuzz storm has passed >:( See you next time!")

# Program created purley by phantom0004, all rights reserved
