<br />
<p align="center">
  <a href="https://github.com/coencoensmeets/Letterboxd-sorter">
    <img src="https://a.ltrbxd.com/logos/letterboxd-decal-dots-neg-rgb.svg" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Letterboxd sorter on colour</h3>

  <p align="center">
    An awesome README template to jumpstart your projects!
    <br />
    <a href="https://github.com/coencoensmeets/Letterboxd-sorter"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/coencoensmeets/Letterboxd-sorter">View Demo</a>
    ·
    <a href="https://github.com/coencoensmeets/Letterboxd-sorter/issues">Report Bug</a>
    ·
    <a href="https://github.com/coencoensmeets/Letterboxd-sorter/issues">Request Feature</a>
  </p>
</p>

## About The Project
The last few months multiple lists became popular on Letterboxd in which the films were sorted by colour. An example: 
[Arlo McLean's list 'color'](https://letterboxd.com/theslayerbuffy/list/color/)
Normally, sorting posters takes lots of time and multiple headaches. This code makes it easy. It sorts all the film a user has seen. It exports an .csv file that can be imported into letterboxd on 
[the new list page](https://letterboxd.com/list/new/) 
 .It also puts out an image of all the colours the code extracted from the poster. The last thing it exports is a plotly graph where all the colours are plotted by RGB value.

### How to use / Example

In the following example my personal Letterboxd account will be used: _(Consider a follow)_ [coencoensmeets](https://letterboxd.com/coencoensmeets/).
The code has only been tested on a windows 10 machine.
First install APIs
1. API installation
  ```sh
  pip install -r requirements.txt
  ```
2. Run the script
  ```sh
  python LB_colour.py D:\\Home\\Data coencoensmeets -LPmI
  ```
  The running of the script has bene built up in the following way:
  ```sh
  python LB_colour.py **Prefered directory** **Username** -**Options**
  ```
  Directory: If the prefered directory can not be found, the current directory will be used.
  Username: This is the letterboxd username (the same username as is in the link to a profile)
  Options: With the many exports, an option has been added to disable a few. If no options are profived, only a list will be added. The options cna be changes by added the letters. The options available:
  1. L: This creates the letterboxd list with the posters sorted that can be imported.
  2. I: Creates the image with the extracted colours sorted.
  3. Pm: Creates the Plotly graph without lines.
  4. Pl: Creates the Plotly graph with lines.

3. Check out the outputs
  <img src="https://preview.redd.it/0tvbgnsck0971.png?width=1904&format=png&auto=webp&s=61341e40b482fad50694cee77aef25c316afa748" alt="Logo" width="400" height="400">
  
