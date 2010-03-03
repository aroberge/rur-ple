# -*- coding: utf-8
""" RUR-PLE: Roberge's Used Robot - a Python Learning Environment
    parser.py - Verifies program files integrity and safety
    Version 0.8.7
    Author: Andre Roberge    Copyright  2005
    andre.roberge@gmail.com
"""

import re
from translation import _

def FixLineEnding(txt):
    # We are going to use Python to interpret these files.
    # Python recognize line endings as '\n' whereas, afaik:
    # Windows uses '\r\n' to identify line endings
    # *nix uses '\n'   (ok :-)
    # Mac OS uses '\r'
    # So, we're going to convert all to '\n'
    txt1 = re.sub('\r\n', '\n', txt) # Windows: tested
    txt = re.sub('\r', '\n', txt1)  # not tested yet: no Mac :-(
    return txt


def ParseProgram(contents):
    # safety check
    safe = "".join(contents)
    safe = safe.replace(")", ")\n")
    safe = safe.replace(":", ":\n")
    safe = safe.replace("(", " (")
    safe_list = safe.split()
    bad_keywords = ["chr", "exec", "eval", "input", "raw_input"]
    for word in bad_keywords:
        if word in safe_list:
            mesg = _("Found a word not allowed: ") + str(word)
            return False, mesg
    return True, ''

def ParseWorld(contents):
    # safety check
    safe = contents[:]
    # only allow known keywords
    keywords = ["avenues", "streets", "walls", "beepers", "robot",
                "'s'", "'S'", '"s"', '"S"',
                "'e'", "'E'", '"e"', '"E"',
                "'w'", "'W'", '"w"', '"W"',
                "'n'", "'N'", '"n"', '"N"', ]
    for word in keywords:
        safe = safe.replace(word, '')
    safe = list(safe)
    no_error = True
    edt_flag = True
    for char in safe:
        if char.isalpha():
            print "problem with world file"
            print "The only allowed words are: "
            for k in keywords:
                print k
            print "This letter was found outside of allowed words:" + char
            no_error = False
            break
    return no_error
