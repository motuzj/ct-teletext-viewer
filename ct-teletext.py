import json
import requests
import argparse
import sys
import os
import re
from colorama import init, deinit, Fore, Back, Style

URL = "https://www.ceskatelevize.cz/teletext-api/v2/text/"

def print_verbose(msg):
    if args.verbose:
        print(msg)

def search_word(word):
    get_teletext_json(URL)
    for page in pages:
        teletext_page = get_teletext_page(page)
        if word in teletext_page:
            # highlight found word in page with red
            teletext_page = teletext_page.replace(word, Fore.RED + word + Style.RESET_ALL)
            print(teletext_page)

def parse_args():
    global args
    parser = argparse.ArgumentParser(
        prog="CT Teletext Viewer",
        description="Viewer for Česká Televize (ČT) teletext. All arguments are optional.")
    parser.add_argument('-p', '--page', type=str, help="go to a specific page")
    parser.add_argument('-s', '--subpage', type=str, help="go to a specific subpage")
    parser.add_argument('-o', '--output', type=str, metavar="FILENAME", help="download whole json teletext for later use and exit")
    parser.add_argument('-i', '--input', type=str, metavar="FILENAME", help="load json teletext from file")
    parser.add_argument('-g', '--search', type=str, metavar="WORD", help="search for specific word in all pages")
    parser.add_argument('-n', '--no-color', action='store_true', help="disable color and formating in output")
    parser.add_argument('-v', '--verbose', action='store_true', help="explain what is being done")

    args = parser.parse_args()

    args_num = len(sys.argv)

    if args.page:
        get_teletext_json(URL)
        print(get_teletext_page(args.page, args.subpage))
        sys.exit()
    elif args.output:
        get_teletext_json(URL)
        sys.exit()
    elif args.search:
        search_word(args.search)
        sys.exit()

def load_teletext_json(filename):
    print_verbose("Loading teletext json from file...")
    load_from_this_file = open(filename, "r")
    return load_from_this_file.read()

def output_teletext_json(filename, text):
    print_verbose("Saving teletext json to file...")
    download_to_this_file = open(args.output, "w")
    download_to_this_file.write(text)
    download_to_this_file.close()

def get_teletext_json(url):
    global pages
    global json_teletext

    # loading from file
    if args.input:
        print_verbose("Fetching teletext from file...")
        try:
            json_text = load_teletext_json(args.input)
        except Exception as e:
            print("Error: ", e)
            sys.exit(1)
    # downloading from url
    else:
        print_verbose("Downloading teletext from url...")
        try:
            json_text = requests.get(url).text
        except requests.exceptions.RequestException as e:
            print(f"Error: There was error accessing a \"{URL}\"! More info: \n{e}")
            sys.exit(1)

    print_verbose("Converting json to python dictionary...")
    try:
        # convert json to dictionary format
        json_teletext = json.loads(json_text)
    except json.decoder.JSONDecodeError as e:
        print(f"Error: Downloaded teletext from \"{URL}\" is not in valid JSON format! More info: \n{e}", file=sys.stderr)
        sys.exit(1)
    
    if args.output:
        output_teletext_json(args.output, json_text)
    
    pages = list(json_teletext["data"].keys())

def get_teletext_page(page_num, subpage=None):
    print_verbose("Parsing teletext content and applying formatting...")
    global subpages
    global current_subpage

    if subpage is None: # true if no page was provided
        try:
            subpages = json_teletext["data"][page_num]["subpages"]
        except KeyError:
            print(f"Page {page_num} doesn't exist. Try to go to page 100.")
            return " "

        if not subpages:
            # page doesn't have any subpages, print the only page
            return get_teletext_page(page_num, "")
        else:
            if len(current_subpage) <= 0:
                current_subpage = subpages[0] # set subpage to first subpage from list
            print_verbose(f"No subpage provided, printing default {current_subpage} subpage.")
            return get_teletext_page(page_num, current_subpage)
    else:
        subpage = subpage.capitalize()
        try:
            output = json_teletext["data"][page_num]["text"][page_num + subpage][5:-6] # parse page from json and strip <pre> tag (with [5:-6])
        except KeyError:
            print(f"Subpage {subpage} doesn't exist for page {page_num}.")
            return " "

        # skip colorizing output
        if args.no_color:
            return output

        # COLORIZING

        # split output to lines for better manipulation
        lines = output.split("\n")

        # colorize a title if there is any
        if lines[0].isspace() and not lines[1].isspace() and lines[2].isspace():
            lines[1] = f"{Fore.CYAN}{lines[1]}{Style.RESET_ALL}" # title
            lines[0] = f"{Fore.BLUE}{'─'*40}{Style.RESET_ALL}"
            lines[2] = f"{Fore.BLUE}{'─'*40}{Style.RESET_ALL}"

        # connect back lines to output
        output = "\n".join(lines)

        # select 3 digit number or 1/2 digit number with dash before it
        pattern = r'(?<!\d)(\d{3})(?=\D|$)|(?<=\d{3}-)(\d{1,2})(?=\D|$)' # this regex was generated by ChatGPT, because I would never have figured that out
        output = re.sub(pattern, r'{}\g<0>{}'.format(Fore.LIGHTCYAN_EX, Style.RESET_ALL), output)
        
        return output

def print_menu(current_page):
    # print list of subpages
    print("Subpages:       ", end=" ")
    if subpages:
        for subpage in subpages:
            if subpage == current_subpage: # print current subpage in color
                print(f"{Fore.LIGHTBLACK_EX}{subpage:^3}", end=" ")
            else:
                print(f"{subpage:^3}", end=" ")
        print("")
    else:
        print() # put cursor to newline

    # print list of 7 nearby pages
    if current_page in pages: # 
        index = pages.index(current_page)
    else:
        index = 0

    num_pages = len(pages)

    if index <= 3:
        near_pages = range(0, 7)  # select first 7 pages
    elif index >= num_pages - 4:
        near_pages = range(num_pages - 7, num_pages) # select last 7 pages
    else:
        near_pages = range(index - 3, index + 4) # select previous 3, current and next 3 pages
    
    print("Pages:          ", end=" ")
    for near_page in near_pages:
        if index == near_page:  # print current page in color
            print(f"{Fore.LIGHTBLACK_EX}{pages[near_page]}", end=" ")
        else:
            print(pages[near_page], end=" ")
    print() # put cursor to new line

init(autoreset=True) # colorama init

# default values
current_page = "100"
current_subpage = ''

parse_args()
get_teletext_json(URL) # load teletext from URL

while True:
    os.system('cls' if os.name == 'nt' else 'clear')

    print(get_teletext_page(current_page))
    
    print_verbose("Displaying navigation menu...")
    print_menu(current_page)

    # get valid input
    while True:
        print_verbose("Waiting for user input...")
        user_input = input("Page or Subpage: ")

        current_subpage = '' # clear current subpage

        if not user_input.isalnum():
            print("Input is not alphanumeric. Please try again.")
            continue

        if user_input.isnumeric():
            current_page = user_input
        else:
            current_subpage = user_input.capitalize()
        break

deinit()
