# Translation howto #
## Introduction ##
You love RUR-PLE and feel it would be a great addition to your country educational pool of applications and tutorials, unfortunately RUR-PLE is not available or only partially translated. Likewise you feel some lessons need improvement or you spotted a typo. Well then you've come to the right page!

## 1. No translation available at all ##
### The basic part ###
An easy way to start which requires little work is just to translate the RUR-PLE Graphical User Interface and the application (HTML) welcome page. This should be quick and entice other translators to join your effort.

This "basic" translation includes TWO files:
  * a ".po" file, added in the proper directory (folder: rur\_locale)
  * a "rur.htm" file, also added in the proper directory (folder: lessons/it); this file is the one displayed in the browser.  Ideally, this last folder should also contain a translation of all the lessons! :-)  At the very least, make a copy of an existing rur.htm file (e.g. the English one) and put it in the appropriate folder.
  * Then you can edit the upper section of rur\_py/translation.py to test locally,

### The lessons ###
#### Images ####
  * Up until lesson 25 only 4 screenshots need to be added to reflect the localized interface. They are:
    * lessons/images/intro/en\_code\_tab.png
    * lessons/images/intro/en\_robot\_window.png
    * lessons/images/intro/en\_status\_bar.png
    * lessons/images/inter/en\_interpreter.png
  * The logic is to:
    * Take the same screenshots of the same windows in your language
      * full window screenshot is not resized: start rurple with the '-s' command line option
      * same for en\_code\_tab.png: no resizing
      * en\_status\_bar.png has 1 program and 1 world file loaded and is resized to 573 width
      * en\_interpreter width depends highly on your language to be able to display the 4 tabs
    * Rename them into language\_code\_filename. For example if you're an Italian translator, your language code is 'it', so the new files will be named it\_code\_tab.png, it\_robot\_window.png and it\_status\_bar.png
    * Place them all in the same lessons/images/intro/ folder
    * Update the image HTML code (lesson 2 and 8) to point to the localized image in the appropriate lesson.

#### HTML pages ####
Coming soon.

#### Tools ####
There is an xml tag with the language in each file and a python script in the lessons folder which enable you to track XML compliance of one language and translation ratio (python checktrans.py es from the lessons folder will give you that for Spanish for example).  The way it works is that you need to copy over all English files into the Spanish folder (don't overwrite existing files, except rurple.css) and start your translation. Once a page is translated change the xml tag from en to es and the script will do the rest.