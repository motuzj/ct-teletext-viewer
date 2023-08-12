import json, requests, sys, os
from colorama import init, deinit, Fore, Back, Style

URL = "https://www.ceskatelevize.cz/teletext-api/v2/text/"

init(autoreset=True)

def parse_args():
    args_num = len(sys.argv)
    if args_num >= 2:
        global current_page
        current_page = sys.argv[1]


def get_teletext_json(url):
    print("Downloading teletext...")
    r = requests.get(url)
    return json.loads(r.text)

def print_teletext_page(page_num, subpage=""):
    try:
        output = json_teletext["data"][current_page]["text"][current_page + subpage][5:-6] # parse page from json and strip <pre> tag (with [5:-6])
    except KeyError:
        print(f"Subpage {current_subpage} doesn't exist for page {current_page}.")
        return
        
    # COLORIZING

    lines = output.split("\n")

    # colorize a title
    if lines[0].isspace() and not lines[1].isspace() and lines[2].isspace():
        lines[1] = f"{Fore.CYAN}{lines[1]}{Style.RESET_ALL}" # title
        lines[0] = f"{Fore.BLUE}{'─'*40}{Style.RESET_ALL}"
        lines[2] = f"{Fore.BLUE}{'─'*40}{Style.RESET_ALL}"

    output = "\n".join(lines)
    
    print(output)

def print_menu(current_page):
    if subpages:
        print("Subpages:       ", end=" ")
        for subpage in subpages:
            if subpage == current_subpage: # print current subpage in color
                print(f"{Fore.LIGHTBLACK_EX}{subpage:^3}", end=" ")
            else:
                print(f"{subpage:^3}", end=" ")
        print("")

    index = pages.index(current_page)
    
    num_pages = len(pages)


    if index <= 3:
        near_pages = range(0, 7)
    elif index >= num_pages - 4:
        near_pages = range(num_pages - 7, num_pages)
    else:
        near_pages = range(index - 3, index + 4)

    print("Pages:          ", end=" ")
    for near_page in near_pages:
        if index == near_page: # print current page in color
            print(f"{Fore.LIGHTBLACK_EX}{pages[near_page]}", end=" ")
        else:
            print(pages[near_page], end=" ")
    print("")

current_page = "100"
current_subpage = 'A'

parse_args()

json_teletext = get_teletext_json(URL)
pages = list(json_teletext["data"].keys())

while True:
    os.system('cls' if os.name == 'nt' else 'clear')

    try:
        subpages = json_teletext["data"][current_page]["subpages"]
    except KeyError:
        print(f"Page {current_page} doesn't exist. Try to go to page 100.")
        continue

    if not subpages:
        # page doesn't have any subpages, print the only page
        print_teletext_page(current_page)
    else:
        print_teletext_page(current_page, current_subpage)
    
    print_menu(current_page)
    user_input = input("Page or Subpage: ")

    current_subpage = 'A'

    if user_input.isnumeric():
        current_page = user_input
    else:
        current_subpage = user_input.capitalize()

deinit()
