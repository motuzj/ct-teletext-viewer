# ČT Teletext Viewer

ČT Teletext Viewer allows you to view teletext content interactively in your terminal.

## Installing

### Linux

You can install this package on Linux by running this command in your terminal:

```bash
python3 -m pip install git+https://github.com/motuzj/ct-teletext-viewer
```

If you are getting `error: externally-managed-environment`, you can install it using [pipx](https://github.com/pypa/pipx) or alternatively you can try adding the `--break-system-packages` switch to the end of the command.

### Windows

On Windows you can install this package using this command, be sure you have [Python](https://www.python.org/downloads/) installed first:

```bash
python -m pip install git+https://github.com/motuzj/ct-teletext-viewer
```

## Usage

Once you have successfully installed the ČT Teletext Viewer, you can lunch it at any time by executing `ct-teletext` (assuming you've correctly set the PATH). By default the program opens interactive mode. Here you can easily navigate through the teletext using numbers (for pages) or letters (for subpages).

## Options

The following options are available:

- `-h` / `--help`: Show this help message and exit.
- `-p PAGE` / `--page PAGE`: Print a specific page and exit.
- `-s SUBPAGE` / `--subpage SUBPAGE`: Print a specific page with subpage and exit, -p option is need for this.
- `-o FILE` / `--output FILE`: Download whole JSON teletext for later use and exit.
- `-i FILE` / `--input FILE`: Load JSON teletext from file.
- `-g WORD` / `--search WORD`: Search for specific word in all pages and it's subpages (case-sensitive)
- `-n` / `--no-color`: Disable color and formating in output.
- `-V` / `--verbose`: Explain what is being done.
- `-v` / `--version`: Show program's version number and exit.

## Screenshots

![Screenshot1](https://github.com/motuzj/ct-teletext-viewer/assets/30744041/03e30014-d6ea-4ee2-8e75-2e465ddc1906)
![Screenshot2](https://github.com/motuzj/ct-teletext-viewer/assets/30744041/67be360c-5cf1-4b3a-94ae-ad78606890db)
