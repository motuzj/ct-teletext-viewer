# ČT Teletext Viewer

ČT Teletext Viewer allows you to view teletext content in your terminal. It supports interactive mode and the use of options.

## Installing

### Linux

You can install this package on Linux by running this command in your terminal:

```bash
python3 -m pip install git+https://github.com/motuzj/ct-teletext-viewer
```

If you are getting `error: externally-managed-environment`, you can install it using [pipx](https://github.com/pypa/pipx) or alternatively you can try adding the `--break-system-packages` switch to the end of the command.

### Windows

You can install this package on Linux by using:

```bash
python -m pip install git+https://github.com/motuzj/ct-teletext-viewer
```

## Usage

Once you have successfully installed the ČT Teletext Viewer, you can lunch it at any time by executing `ct-teletext` (assuming you've correctly set the PATH). By default the program opens interactive mode. Here you can easily navigate through the teletext using numbers (for pages) or letters (for subpages).

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

## Screenshots

![Screenshot1](https://github.com/motuzj/ct-teletext-viewer/assets/30744041/03e30014-d6ea-4ee2-8e75-2e465ddc1906)
![Screenshot2](https://github.com/motuzj/ct-teletext-viewer/assets/30744041/67be360c-5cf1-4b3a-94ae-ad78606890db)
