import json
import requests
import argparse
import sys
import os
import re
from colorama import init, deinit, Fore, Style

VERSION = "0.2.2"
URL = "https://www.ceskatelevize.cz/teletext-api/v2/text/" # url of json teletext file
DEFAULT_PAGE = "100"

class CTTeletextViewer:
    def __init__(self, args):
        self.args = args
        self.pages = []
        self.json_teletext = ""
        self.current_subpages = []
        self.current_subpage = ""
        self.current_page = DEFAULT_PAGE

    def print_verbose(self, msg):
        """
        Prints verbose message if it is enabled.

        Parameters:
            msg: Usually a string that will be printed.
        """
        if self.args.verbose:
            print(msg)

    def search_word(self, word):
        """
        Search in all teletext pages for certain word and highlight it in red.
        
        Parameters:
            word: A word/words you want to search for.
        """
        self.get_json(URL)

        for page in self.pages:
            self.get_page(page)
            subpages = self.current_subpages if self.current_subpages else [None]
            for subpage in subpages:
                content = self.get_page(page, subpage)
                if word in content:
                    # highlight found word in page with red
                    self.print_verbose(f"A word \"{word}\" was found in {page}, formatting and printing that page...")
                    print(self.format_page(content))

    def load_json(self, filename):
        """
        Returns teletext from local json file
        
        Parameters:
            filename (string): Path to the json file.
        
        Returns:
            string: Contents of the file.
        """
        self.print_verbose("Loading teletext json from file...")
        with open(filename, "r") as f:
            return f.read()

    def output_teletext_json(self, filename, text):
        """
        Saves teletext to json file.

        Parameters:
            filename (string): Path where you want to save the file.
        """
        self.print_verbose("Saving teletext json to file...")
        with open(filename, "w") as f:
            f.write(text)

    def get_json(self, url):
        """
        Downloads and saves a teletext in Python dictionary format.

        Parameters:
            url: URL to the json teletext file.
        """

        # loading from file
        if self.args.input:
            self.print_verbose("Fetching teletext from file...")
            try:
                json_text = self.load_json(self.args.input)
            except Exception as e:
                print(f"Error: {e}", file=sys.stderr)
                sys.exit(1)
        # downloading from url
        else:
            self.print_verbose("Downloading teletext from url...")
            try:
                json_text = requests.get(url).text
            except requests.exceptions.RequestException as e:
                print(f"Error: There was error accessing a \"{URL}\"! More info: \n{e}", file=sys.stderr)
                sys.exit(1)

        self.print_verbose("Converting json to python dictionary...")
        try:
            # convert json to dictionary format
            self.json_teletext = json.loads(json_text)
        except json.decoder.JSONDecodeError as e:
            print(f"Error: Downloaded teletext from \"{URL}\" is not in valid JSON format! More info:\n{e}", file=sys.stderr)
            sys.exit(1)
        
        if self.args.output:
            self.output_teletext_json(self.args.output, json_text)
        
        self.pages = list(self.json_teletext["data"].keys())

    def get_page(self, page_num, subpage=None):
        """
        Gets a page by the specified page number and subpage name.

        Parameters:
            page_num: Number of a page.
            subpage: Optional subpage name.

        Returns:
            string: Formatted or unformatted page content.
        """
        self.print_verbose("Parsing teletext page content...")

        # fetch list of subpages
        try:
            self.current_subpages = self.json_teletext["data"][page_num]["subpages"]
        except KeyError:
            print(f"Page {page_num} doesn't exist. Try going to page {DEFAULT_PAGE}.")
            return None

        if not subpage:
            if not self.current_subpages:
                # page doesn't have any subpages, print the only page
                subpage = ""
            else:
                self.current_subpage = self.current_subpages[0] # set current_subpage to first avaible subpage
                self.print_verbose(f"No subpage provided, printing default {self.current_subpage} subpage.")
                subpage = self.current_subpage
        
        try:
            output = self.json_teletext["data"][page_num]["text"][page_num + subpage][5:-6] # parse page from json and strip <pre> tag
        except KeyError:
            print(f"Subpage {subpage} doesn't exist for page {page_num}.")
            return " "

        # skip colorizing output
        if self.args.no_color or self.args.search:
            return output
        
        return self.format_page(output)

    def format_page(self, page_content):
        """
        Formats given page content with colors.

        Parameters:
            current_page: Current page number.

        Returns:
            string: Formatted page content.
        """
        self.print_verbose("Applying formatting to a page...")
        # COLORIZING
        # split page_content to lines for better manipulation
        lines = page_content.split("\n")

        # colorize a title if there is any
        if lines[0].isspace() and not lines[1].isspace() and lines[2].isspace():
            lines[1] = f"{Fore.CYAN}{lines[1]}{Style.RESET_ALL}" # title
            lines[0] = f"{Fore.BLUE}{'─'*40}{Style.RESET_ALL}"
            lines[2] = f"{Fore.BLUE}{'─'*40}{Style.RESET_ALL}"

        # connect back lines to page_content
        page_content = "\n".join(lines)

        # format page numbers in page_content: select 3 digit number or 1/2 digit number with dash before it and print it
        pattern = r'(?<!\d)(\d{3})(?=\D|$)|(?<=\d{3}-)(\d{1,2})(?=\D|$)' # this regex was generated by ChatGPT
        page_content = re.sub(pattern, r'{}\g<0>{}'.format(Fore.LIGHTCYAN_EX, Style.RESET_ALL), page_content)
        return page_content

    def print_menu(self, current_page):
        """
        Prints menu with list of subpages and pages.

        Parameters:
            current_page: Current page number.
        """
        # print list of subpages
        print("Subpages:", end=" ")
        if self.current_subpages:
            for subpage in self.current_subpages:
                if subpage == self.current_subpage: # print current subpage in color
                    print(f"{Fore.LIGHTBLACK_EX}{subpage}{Style.RESET_ALL}", end=" ")
                else:
                    print(f"{subpage}", end=" ")
        print()

        # print list of 7 nearby pages
        if current_page in self.pages: # 
            index = self.pages.index(current_page)
        else:
            index = 0

        num_pages = len(self.pages)

        if index <= 3:
            near_pages = range(0, 7)  # select first 7 pages
        elif index >= num_pages - 4:
            near_pages = range(num_pages - 7, num_pages) # select last 7 pages
        else:
            near_pages = range(index - 3, index + 4) # select previous 3, current and next 3 pages
        
        print("Pages:", end=" ")
        for near_page in near_pages:
            if index == near_page:  # print current page in color
                print(f"{Fore.LIGHTBLACK_EX}{self.pages[near_page]}{Style.RESET_ALL}", end=" ")
            else:
                print(self.pages[near_page], end=" ")
        print()

    def main(self):
        """Main program loop"""
        self.get_json(URL)
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')

            print(self.get_page(self.current_page, self.current_subpage))
            
            self.print_verbose("Displaying navigation menu...")
            self.print_menu(self.current_page)

            # get valid input
            while True:
                self.print_verbose("Waiting for user input...")
                try:
                    user_input = input("Page or Subpage: ")
                except KeyboardInterrupt:
                    print()
                    deinit()
                    sys.exit()

                self.current_subpage = '' # clear current subpage

                if user_input.isnumeric():
                    self.current_page = user_input
                elif user_input.isalpha():
                    self.current_subpage = user_input.upper()
                else:
                    print("Input is not alphanumeric. Please try again.")
                    continue
                break

def main():
    parser = argparse.ArgumentParser(
        prog="CT Teletext Viewer",
        description="Viewer for Česká Televize (ČT) teletext. All arguments are optional."
    )
    parser.add_argument('-p', '--page', type=str, help="print a specific page and exit")
    parser.add_argument('-s', '--subpage', type=str, help="print a specific page with subpage and exit, -p option is need for this")
    parser.add_argument('-o', '--output', type=str, metavar="FILENAME", help="download the whole JSON teletext for later use and exit")
    parser.add_argument('-i', '--input', type=str, metavar="FILENAME", help="load JSON teletext from a file")
    parser.add_argument('-g', '--search', type=str, metavar="WORD", help="search for a specific word in all pages and it's subpages (case-sensitive)")
    parser.add_argument('-n', '--no-color', action='store_true', help="disable color and formatting in output")
    parser.add_argument('-V', '--verbose', action='store_true', help="explain what is being done")
    parser.add_argument('-v', '--version', action='version', version=f"%(prog)s {VERSION}")

    args = parser.parse_args()
    viewer = CTTeletextViewer(args)

    if args.page:
        viewer.get_json(URL)
        print(viewer.get_page(args.page, args.subpage))
        sys.exit()
    elif args.output:
        viewer.get_json(URL)
        sys.exit()
    elif args.search:
        viewer.search_word(args.search)
        sys.exit()

    if not sys.stdout.isatty():
        print("Error: The program requires a terminal for interactive mode. Use instead arguments --page and --subpage (optional)", file=sys.stderr)
        sys.exit(1)
    viewer.main()

if __name__ == "__main__":
    init(autoreset=True)
    main()
    deinit()
