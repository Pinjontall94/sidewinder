![Sidewinder Logo](https://github.com/Pinjontall94/sidewinder/blob/main/sidewinder.png)
# Sidewinder
An open source static site generator with an emphasis on code readability, written in Python!
Easily turn markdown and html pages into a cohesive website with consistent theming.

## Installation
1. Install [python 3](https://www.python.org/) if it's not already on your computer
2. Download the latest sidewinder release and extract the zip file
3. Navigate to your extracted sidewinder folder
4. (Optional, Linux-only) If you'd like to have a desktop entry for sidewinder
you can run from your app launcher directly:
    1. Copy the `Sidewinder.desktop` file to `$HOME/.local/share/applications/`
    2. Edit that copy such that `Path` key equals the full path to this folder
    3. Copy the sidewinder png icon to `$HOME/.icons/` (make the folder if you need to)
    4. Log out and log back in, or run `update-desktop-database` in a terminal

## Usage
1. Place markup files (either [markdown](https://www.markdownguide.org/) or 
[html](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content))
in the content folder.
2. (Optional) Edit the file named `template.html` to taste (keeping the 
`{{ Title }}` and `{{ Content }}` strings intact) 
3. Run sidewinder:
    - Windows: Double click `sidewinder.bat`
    - MacOS: Double click `sidewinder.command`
    - Linux: Right click `sidewinder.sh` and select the option `Run as program`
4. Sidewinder will then create a new folder called `public` and compile your
site there

## Hosting Locally
To view the site locally, open the `public` folder, open a terminal or cmd.exe
window there, and run the following (cross-platform):
```sh
python -m http.server 8080
```
While this runs in the terminal window, your site will be visible
[here](http://localhost:8080) (or just enter `localhost:8080` into your
browser window)

## Static Assets
All static assets (CSS styling, images, icons, other media) will be copied from
the `static` folder into the root of `public` (keep that in mind for any local
hrefs or CSS `url(...)` directives).
