#Welcome wiki page of the project

# Introduction #

RUR-PLE is very similar to GVR, but RUR-PLE can use all Python features (while GVR only limited subset of syntax). RUR-PLE has 48 lessons (in main European languages and Chinese) with the code and robot environment examples to experiment with.

# Lessons and languages available #
## Stable release (v1.0.1) ##
  * UI: 7 languages (English, Spanish, German, Welsh, Chinese, French, Turkish)
  * Lessons: 3 languages (English, Chinese, Turkish @ 85%)
  * Number of lessons: 48

## SVN repository ##
  * UI: 8 languages (English, Spanish, German, Welsh, Chinese, French, Turkish, Italian)
  * Lessons: 6 languages (English, Chinese, German, Turkish @ 85%, Spanish up to lesson 10, French WIP)
  * Number of lessons: 53 not all merged (WIP) nor translated


# Mailing List #

We use Google Groups to communicate and the group is https://groups.google.com/group/rur-ple-discuss

# Translation #
A "basic" translation includes TWO files:
  * a ".po" file, added in the proper directory (folder: rur\_locale)
  * a "rur.htm" file, also added in the proper directory (folder: lessons/it); this file is the one displayed in the browser.  Ideally, this last folder should also contain a translation of all the lessons! :-)  At the very least, make a copy of an existing rur.htm file (e.g. the English one) and put it in the appropriate folder.
  * Then you can edit the upper section of rur\_py/translation.py to test locally

More soon about how to translate the lessons. Those are all HTML pages and we're currently looking into how to make it easier for translator to provide help without having to care about the file structure. We are also migrating to XHTML and reviewing some slight markup bugs, so you might want to hold on a bit longer before starting to translate (Dec-31-2009).