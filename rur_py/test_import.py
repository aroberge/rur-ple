# -*- coding: utf-8
# test_import.py

import re
from translation import _

isolate_words = re.compile(r'\W+')  # used with .split()

# pre-compiled some regular expression with allowable use of "import"
imp_use = re.compile('^import useful', re.MULTILINE)
imp_use_as = re.compile('^import useful as (\w+)', re.MULTILINE)
from_use_imp_star = re.compile('^from useful import \*', re.MULTILINE)
from_use_imp_names = re.compile("^from useful import (\w+(,[ ]*\w+)*)", re.MULTILINE)
from_use_imp_as = re.compile("^from useful import (\w+) as (\w+)", re.MULTILINE)

# In the following, "r" is used so that \b identifies a word boundary,
# and is not interpreted as backslash by Python.
import_misuse = re.compile(r'\bimport\b', re.MULTILINE)

# use to commenting out the valid "import" statements after processed.
comment_from = re.compile('^from ', re.MULTILINE)
comment_import = re.compile('^import ', re.MULTILINE)

# Create a fake module which can be "imported"

right = "turn_right():\n"+\
        "    turn_left()\n"+\
        "    turn_left()\n"+\
        "    turn_left()\n\n"

around = "turn_around():\n"+\
        "    turn_left()\n"+\
        "    turn_left()\n\n"

up_east = "climb_up_east():\n"+\
        "    turn_left()\n"+\
        "    move()\n"+\
        "    turn_left()\n"+\
        "    turn_left()\n"+\
        "    turn_left()\n\n"

up_west = "climb_up_west():\n"+\
        "    turn_left()\n"+\
        "    turn_left()\n"+\
        "    turn_left()\n"+\
        "    move()\n"+\
        "    turn_left()\n\n"

down_west =  "climb_down_west():\n"+\
        "    turn_left()\n"+\
        "    move()\n"+\
        "    turn_left()\n"+\
        "    turn_left()\n"+\
        "    turn_left()\n\n"

down_east =  "climb_down_east():\n"+\
        "    turn_left()\n"+\
        "    turn_left()\n"+\
        "    turn_left()\n"+\
        "    move()\n"+\
        "    turn_left()\n\n"

commands = {'turn_right': right, 'turn_around': around,
            'climb_up_east': up_east, 'climb_up_west': up_west,
            'climb_down_east': down_east, 'climb_down_west': down_west}

# end of info on fake module

# The following fonctions will process the "import" statement to
# add the "imported commands" before the "import" statement
# before commenting out (by pre-pending #) the "import" statement line
def import_useful():
    added_text = ''
    for instruction in commands:
        new = "def " + 'useful.' + commands[instruction]
        added_text += new
    return added_text, True

def from_useful_import_star():
    added_text = ''
    for instruction in commands:
        new = "def " + commands[instruction]
        added_text += new
    return added_text, True

def import_useful_as(syn):
    added_text = ''
    for instruction in commands:
        new = "def " + syn + '.' + commands[instruction]
        added_text += new
    return added_text, True

def from_useful_import_names(names):
    added_text = ''
    for instruction in isolate_words.split(names):
        try:
            new = "def " + commands[instruction]
        except:
            print instruction, _(' not found in module useful.')
        added_text += new
    return added_text, True

def from_useful_import_as(name, syn):
    added_text = ''
    try:
        new = "def " + commands[name].replace(name, syn)
    except:
        print name, _(' not found in module useful.')
    added_text += new
    return added_text, True

def process_no_import():
    added_text = ''
    return added_text, True

# the basic processing function

def process_file(file_text):
    if imp_use_as.search(file_text):    # look for "import useful as ..."
        syn = imp_use_as.findall(file_text)
        added_text, safe_import_flag = import_useful_as(syn[0])
        file_text = comment_import.sub('#import ', file_text)
    elif imp_use.search(file_text):   # perhaps the "as ..." part is missing
        added_text, safe_import_flag = import_useful()
        file_text = comment_import.sub('#import ', file_text)
    elif from_use_imp_star.search(file_text):
        added_text, safe_import_flag = from_useful_import_star()
        file_text = comment_from.sub('#from ', file_text)
    elif from_use_imp_as.search(file_text):
        names = from_use_imp_as.findall(file_text)
        name = names[0][0]
        syn = names[0][1]
        added_text, safe_import_flag = from_useful_import_as(name, syn)
        file_text = comment_from.sub('#from ', file_text)
    elif from_use_imp_names.search(file_text):
        names = from_use_imp_names.findall(file_text)
        added_text, safe_import_flag = from_useful_import_names(names[0][0])
        file_text = comment_from.sub('#from ', file_text)
    elif import_misuse.search(file_text):
        safe_import_flag = False
        file_text = ''   # remove it all
        added_text = '# import keyword used improperly'
        print _('import keyword used improperly')
    else:
        added_text = ''
        safe_import_flag = True  # nothing found

    added_text += file_text
    return added_text, safe_import_flag

#======== Various test cases == only self-testing stuff follows

test1 = '''# test1: no import
other instructions'''

test2 = '''# test2
import useful
other instructions'''

test3 = '''# test3
from useful import *
other instructions'''

test4 = '''# test4
from useful import turn_around, turn_right, climb_up_east
other instructions'''

test5 = '''# test5
import useful as use
other instructions'''

test6 = '''# test6
from useful import turn_right
other instructions'''

test7 = '''# test6
from useful import turn_right
other instructions'''

test8 = '''# test8
from useful import turn_right as vire_a_droite
other instructions'''

test9 = '''# test9
import sys
other instructions'''

test10 = '''# test10
from sys import *
other instructions'''

test11 = '''# test11
# import in comment
import useful
other instructions'''

test12 = '''# test12
important test'''

test13 = '''# test 13
import useful
# import sys
other instructions'''

test14 = '''# test14: two import statements; good one first
import useful
import sys
other instructions'''

test15 = '''# test15: two import statements; bad one first
import useful
import sys
other instructions'''

test16 = '''# test16: bad import, indented

        import sys
other instructions'''

if __name__ == "__main__":
    print "=====begin 1: no import======"
    added_text, safe_import_flag = process_file(test1)
    print added_text
    print "safe import flag = ", safe_import_flag
    print "=====begin 2======"
    added_text, safe_import_flag = process_file(test2)
    print added_text
    print "safe import flag = ", safe_import_flag
    print "=====begin 3======"
    added_text, safe_import_flag = process_file(test3)
    print added_text
    print "safe import flag = ", safe_import_flag
    print "=====begin 4======"
    added_text, safe_import_flag = process_file(test4)
    print added_text
    print "safe import flag = ", safe_import_flag
    print "=====begin 5======"
    added_text, safe_import_flag = process_file(test5)
    print added_text
    print "safe import flag = ", safe_import_flag
    print "=====begin 6======"
    added_text, safe_import_flag = process_file(test6)
    print added_text
    print "safe import flag = ", safe_import_flag
    print "=====begin 7======"
    added_text, safe_import_flag = process_file(test7)
    print added_text
    print "safe import flag = ", safe_import_flag
    print "=====begin 8======"
    added_text, safe_import_flag = process_file(test8)
    print added_text
    print "safe import flag = ", safe_import_flag
    print "=====begin 9: import not allowed======"
    added_text, safe_import_flag = process_file(test9)
    print added_text
    print "safe import flag = ", safe_import_flag
    print "=====begin 10: import not allowed======"
    added_text, safe_import_flag = process_file(test10)
    print added_text
    print "safe import flag = ", safe_import_flag
    print "=====begin 11: import ok in text and import in comment======"
    added_text, safe_import_flag = process_file(test11)
    print added_text
    print "safe import flag = ", safe_import_flag
    print "=====begin 12: word used: important; should be ok ======"
    added_text, safe_import_flag = process_file(test12)
    print added_text
    print "safe import flag = ", safe_import_flag
    print "=====begin 13: 2nd import in comment ======"
    added_text, safe_import_flag = process_file(test13)
    print added_text
    print "safe import flag = ", safe_import_flag
    print "=====begin 14: two import statements; good one first ======"
    added_text, safe_import_flag = process_file(test14)
    print added_text
    print "safe import flag = ", safe_import_flag
    print "=====begin 15: two import statements; bad one first ======"
    added_text, safe_import_flag = process_file(test15)
    print added_text
    print "safe import flag = ", safe_import_flag
    print "=====begin 16: bad import, indented ======"
    added_text, safe_import_flag = process_file(test16)
    print added_text
    print "safe import flag = ", safe_import_flag
    print "====="
    wait = input("Press enter to exit.")
