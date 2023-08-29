# ČT Teletext Viewer

ČT Teletext Viewer allows you to view teletext content in your terminal.

## Usage

1. Clone or download this repository.
2. Navigate to the project directory using terminal.
3. Make sure you have Python 3 installed.
4. Install required packages by running following command:

    ```shell
    pip install -r requirements.txt
    ```

5. Run the viewer

    On Windows:

    ```shell
    python ct-teletext.py
    ```

    On Linux:

    ```shell
    python3 ct-teletext.py
    ```

## Options

The following options are available:

- `-h` / `--help`: Show this help message and exit.
- `-p` / `--page`: Go to a specific page.
- `-s` / `--subpage`: Go to a specific subpage.
- `-o` / `--output`: Download whole json teletext for later use and exit.
- `-i` / `--input`: Load json teletext from file.
- `-g` / `--search`: Search for specific word in all pages.
- `-n` / `--no-color`: Disable color and formating in output.
- `-v` / `--verbose`: Explain what is being done.
