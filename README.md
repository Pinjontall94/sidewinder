# Sidewinder
An open source static site generator with an emphasis on code readability, written in Python!
Easily turn markdown and html pages into a cohesive website with consistent theming.

## Installation

1. Clone the directory with git
2. `python -m venv venv`
3. `source venv/bin/activate.sh`
4. `python -m pip install -r requirements.txt`

## Usage

Place markup in the content page and simply run `./main.sh` to compile the new 
static site and locally host on port 8888. The static site will generate in the 
new `public` folder for you to host!

All static assets (CSS styling, images, icons, other media) will be copied from
the `static` folder into the root of `public` (keep that in mind for any local
hrefs or CSS `url(...)` directives).

## TODO

- Create Windows batch file equivalent of `main.sh` for `cmd.exe`
