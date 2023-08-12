import json, requests, os, time
from colorama import just_fix_windows_console
just_fix_windows_console()

def print_teletext_page(page_num, subpage=""):
    output = json_teletext["data"][current_page]["text"][current_page + subpage][5:-6] # parse page from json and strip <pre> tag (with [5:-6])
    
    # COLORIZING

    lines = output.split("\n")

    # colorize a title
    lines[1] = "\033[36m" + lines[1] + "\033[0m"

    output = "\n".join(lines)
    print(output)

def print_menu(current_page):
    if subpages:
        for subpage in subpages:
            if subpage == current_subpage: # print current subpage in color
                print(f"\033[90m{subpage}\033[0m", end=" ")
            else:
                print(subpage, end=" ")
        print("")

    index = pages.index(current_page)
    near_pages = range(max(0, index - 3), min(index + 4, len(pages)))

    for near_page in near_pages:
        if index == near_page: # print current page in color
            print(f"\033[90m{pages[near_page]}\033[0m", end=" ")
        else:
            print(pages[near_page], end=" ")
    print("")


url = 'https://www.ceskatelevize.cz/teletext-api/v2/text/'
r = requests.get(url, allow_redirects=True)

json_teletext = json.loads(r.text)
pages = list(json_teletext["data"].keys())

current_page = 100
current_subpage = 'A'

while True:
    current_page = input("Page: ")
    os.system('clear')

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
