# (c) 2008 - Peter Maas
# v.1.1
# checktrans.py
#    Little tool to check XML-conformance of the lessons and also
#    the translated part in percent (need to add lang attributes 
#    to the html tag of completely translated lessons).
# GPLv2

from xml.etree import ElementTree as ET
import xml.parsers.expat
import os
import sys

def checklang(f):
    try:
        doc = ET.parse(f)
        root = doc.getroot()
        if root.attrib.has_key("lang"):
            return root.attrib["lang"]
        else:
            return "?"
    except xml.parsers.expat.ExpatError, e:
        print f + " is not a valid XHTML file."
        print ">>>>>>>>>" + str(e)
        return "?"
    
try:
    d = sys.argv[1]
except IndexError:
    print "Missing directory argument."
    sys.exit(1)

total_size = 0
tr_size = 0
total_files = 0
tr_files = 0
lang = d
extension = '.htm'
show_files = True

for d, subd, subf in os.walk(d):
    for f in subf:
        if f.endswith(extension):
            fa = os.path.normpath(os.path.join(d, f))
            try:
                fsize = os.path.getsize(fa)
                flang = checklang(fa)
                if flang == lang:
                    tr_size += fsize
                    tr_files += 1
                total_size += fsize
                total_files += 1
                if show_files:
                    print "file %s, lang = %s, size = %d" % (fa, flang, fsize)
            except Exception, e:
                print ">>>>>>>>>" + str(e)

print "%s-files: %d, %s/%s-files : %d" % (extension, total_files, extension, lang, tr_files)
print "files complete: %.2f %%" % (100.*tr_files/total_files)
print "%s-size: %d, %s/%s-size : %d" % (extension, total_size, extension, lang, tr_size)
print "size complete: %.2f %%" % (100.*tr_size/total_size)
