# Example URLS for testing ethically: http://testphp.vulnweb.com  or  https://vulnerable-website.com/
# ---------------------------------------------------------------------------------------
# This program, created by Phantom, is intended for ethical and responsible security
# testing only. Use it exclusively on systems where you have explicit authorization.
# Unauthorized use of this software is illegal and unethical.
# ---------------------------------------------------------------------------------------
# Check me out on GitHub! -> https://github.com/phantom0004
#---------------------------------------------------------------------------------------
try:
    import requests
    from termcolor import colored
    from bs4 import BeautifulSoup, Comment
    import uuid
except ModuleNotFoundError as error_message:
    exit(f"You are missing the following library, please install in terminal using 'pip install <module name>' : {error_message}")
import os
import time
import sys

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
    global log_file, redirect_counter # Define global variables needed
    
    with open(wordlist_path, "r") as wordlist:
        for word in wordlist: 
            word = word.strip()
            fuzzing_link = normalize_url(f"{website_link}/{word}") # Normalize fuzzing link in hopes to eliminate redirections 
            
            try:
                time.sleep(float(delay)) # Prevent "too many requests" status code or else even a potential website block 
            except KeyboardInterrupt:
                break 
            
            try:
                res = requests.get(url=f"{fuzzing_link}", allow_redirects=False)
                redirect_output = check_for_redirects(res, redirect_counter,fuzzing_link)
                if res.status_code == 404: continue
                
                if redirect_output[0] == True:
                    if verbose == "Y" and write_to_file == False:
                        print(f"[!] Server is redirecting requests, adding delay to try prevent this. [Redirection Link {colored(redirect_output[1], 'green')}]")
                    elif verbose == "Y" and write_to_file == True:
                        log_to_file(f"[!] Server is redirecting requests, adding delay to try prevent this. [Redirection Link {redirect_output[1]}]\n", log_file) 
                    
                    fuzzing_link = normalize_url(fuzzing_link) # Update fuzzing link to remove the trailing slash
                    
                elif redirect_output[0] == "redirect_fail":
                    exit("Server keeps redirecting, this is possibly due to the fact that it has noticed the fuzzing attempts")
                    
            except KeyboardInterrupt:
                break
            except TimeoutError:
                print("Connection timeout, skipping . . .")
                continue
            except requests.RequestException as res_error:
                print(f"[-] An exception occured within the requests library - {res_error}")
                break
            
            if write_to_file == "Y" : print() # Reduce clutter from abpve verbose output
            print("[+] DIRECTORY FOUND : " + colored(word, "green") + f"    [Full Link : {fuzzing_link}]")    
            if write_to_file == True: log_to_file(f"\n[+] DIRECTORY FOUND : {word} [Full Link : {fuzzing_link}]\n", log_file)
             
            if verbose == "Y": 
                parse_verbose_output(res, write_to_file, log_file)
    
def verbose_output(html_content):
    links, titles, comments, forms = [], [], [], []
    
    for link in html_content.find_all("a"):
        try:
            href = link.get('href') # Different logic for links as stripping normally doesnt work always
            if href and len(href) > 1:
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
        return f"[ERROR INFO] Website returned a status that is not 200 : {website_error_messages[response]} [Status : {response}]"
    else:
        return None

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

def check_for_redirects(response, redirections_happened, full_url):
    if redirections_happened[0] >= 8:
        return "redirect_fail", None  # Max redirections reached

    redirect_flag = False  # Indicates if a redirection occurred

    # Check if link was re-used in history
    if response.history:
        for previous_response in response.history:
            if full_url in previous_response.url:
                redirect_flag = True
                break

    # Check current response for a new redirect status
    if response.status_code in range(300, 399):
        redirect_flag = True

    if not redirect_flag:
        redirections_happened[0] = 0
        return False, None

    # Handle redirection
    redirections_happened[0] += 1
    delay_time = 2 * redirections_happened[0]
    time.sleep(delay_time)
    
    try:
        redirected_url = response.headers.get('Location')
    except:
        redirected_url = "Unable to identify the location of the redirect"
    return True, redirected_url

def normalize_url(full_url):
    if full_url.endswith('/'):
        return full_url[:-1]
    else:
        return full_url + '/'

def clear_terminal():    
    print("[+] OPTIONS SELECTED, Cleaning terminal and starting FuzzFindr . . .")
    time.sleep(3) # Allow user to read message and other above content
    
    # Execute the appropriate command based on the operating system
    command = "cls" if os.name == 'nt' else "clear"
    result = os.system(command)
    
    if result != 0:
        print("[-] Failed to clear the terminal. Continuing without clearing \n\n")
    else:
        display_banner()

def parse_verbose_output(res, write_to_file, log_file):
    html_extracted = True
    try:
        if res.content and 'text/html' in res.headers.get('Content-Type', ''):
            html_extract = BeautifulSoup(res.content, "html.parser") # Extract HTML code from website
        else:
            if write_to_file == True: 
                log_to_file("[-] Non-HTML content received or empty response\n", log_file)
            if write_to_file == False:
                print(colored("[-] Non-HTML content received or empty response\n", "red"))
            html_extracted = False
    except:
        print(colored(f"[-] Unable to extract HTML from website [Status Code Retrieved : {res.status_code}] \n", "red"))
        if write_to_file == True: log_to_file(f"[-] Unable to extract HTML from website [Status Code Retrieved : {res.status_code}]\n", log_file)
    finally:
        error_check_output = error_check(res.status_code)
        if error_check_output is not None:
            if write_to_file == False:
                print(error_check_output)
            elif write_to_file == True:
                log_to_file(error_check_output+"\n", log_file)
    
    if html_extracted == False : return
    
    stored_links, stored_titles, stored_comments, stored_forms = (verbose_output(html_extract))
    if stored_links is None and stored_titles is None and stored_comments is None and stored_forms is None:
        print(colored("[-] No data was able to be extracted for this section \n", "red"))
        if write_to_file == True: log_to_file(f"[-] No data was able to be extracted for this section \n", log_file)
    else: 
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
    if write_to_file == True: log_to_file("\n\n", log_file)
    else: print()

display_banner()

# Program required variables
website_link, wordlist_path = handle_user_arguments()
verbose_log_flag, log_file = False, None
redirect_counter = [0]

if website_link is None or wordlist_path is None:
    exit("[-] Incorrect usage detected. Please run the program as follows: python3 fuzzfindr.py <website_link> <wordlist_path>\n"
     "Example: python3 fuzzfindr.py http://vulnerablewebsite.com fuzz_wordlist.txt\n\n"
     "For more information, check: https://github.com/phantom0004/FuzzFindr-Web-Fuzzing-Tool")

try:
    if (file := open(wordlist_path, "r")): file.close()
except FileNotFoundError or OSError:
    exit("[-] Wordlist cannot be found, ensure directory is valid and format is a text file")

if website_link[-1:] == "/": website_link = website_link[:-1]

verbose_option = input("The verbose option displays HTML content on the screen. Enable verbose option? [Y/N] (Default is 'N'): ").upper()
if verbose_option == "Y":
    print(colored("[!] Verbose option is slower as it will return a detailed output [displays links, titles, comments and forms]\n", 'yellow', attrs=['bold']))
    
    verbose_log_option = input("Do you want to log verbose output silently to a file? [Y/N] (Default is 'N'): ").upper()
    if verbose_log_option == "Y":
        print(colored("[!] Verbose option set to True. Verbose logs will not be shown in terminal but saved in a text file\n", 'yellow', attrs=['bold']))
        
        verbose_log_flag, log_file = True, "fuzzfindr_log-"+str(uuid.uuid4())[:6] + ".txt"
    else:
        print(colored(f"[!] Verbose output will be displayed on terminal only\n", 'yellow', attrs=['bold']))

try:
    delay_option = float(input("Enter a delay in seconds to have a pause in between of requests (Default is '0' seconds): "))
    if delay_option < 0: delay_option = 0
except:
    delay_option = 0
finally:
    print(colored(f"[!] Delay option set to {delay_option} seconds\n", 'yellow', attrs=['bold']))

clear_terminal() # Clear above clutter and display banner again

print(colored(f"[!] Started Fuzzing at : {fetch_time()} [Press ctrl+c to abort]", attrs=['bold']))
start_fuzzer(wordlist_path, website_link, delay_option, verbose_option, verbose_log_flag)

print(colored(f"[!] Fuzzing ended at : {fetch_time()}", attrs=['bold']))
if log_file is not None: print(colored(f"[+] Verbose log file saved at : {log_file} (Stored same directory as fuzzfindr)", 'green'))
    
print("\nThe fuzz storm has passed >:( See you next time!")
# Program created purley by phantom0004, all rights reserved
