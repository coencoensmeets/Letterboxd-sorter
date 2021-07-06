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
  The graph with lines:
  <img src="https://preview.redd.it/0tvbgnsck0971.png?width=1904&format=png&auto=webp&s=61341e40b482fad50694cee77aef25c316afa748" alt="Logo" width="800" height="400">
  The image with sorted colours:
  <img src="https://i.imgur.com/ACaDdRc.png" alt="Logo">
  
### Possible updates:
  By plotting the RGB values in a 3D plot with lines that connect adjacent posters, shows issues with yellow and reds. One sorting method that might fix that is by first K-clustering all the values into groups and then connecting the groups. This way the yellows are not mixed in with the whites.

### Errors in sorting:
Unfortunately, there are some apparent errors. Colour is interpreted in the brain and is influenced by many factors. The first issue is getting one single RGB value from a poster. What colour is leading in the image?Secondly, sorting colours is an impossible job to get correct and certainly for a machine. Alan Zucconi wrote a great article about it. 
([https://www.alanzucconi.com/2015/09/30/colour-sorting/](https://www.alanzucconi.com/2015/09/30/colour-sorting/)) I used his inverted step sorting algorithm because it seemed to give the best results.

### The workings:
Because of the limited acces to the Letterboxd API. The films are webscraped. Due to the limited information possible to gather from the films site, an algorithm was created to calculate a possible poster url. If this url does not exist a more time sensitive algorithm is used, that downloads a new site and extracts the poster url from that. After all the posters and films are collected. Each poster is evaluated with its main, dominant colour. These colours are later used to order the poster using the inverted step algorithm created by Alen Zucconi. After the lists are sorted the options are evaluated and the files are outputted as desired. If the data, of previous runs of the code, is in the directory that is being used, the list of films will only be updated. Within the code there are also options to not only update but start fresh. This option has to be activated in the code itself.
