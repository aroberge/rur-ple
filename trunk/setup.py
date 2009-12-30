#!/usr/bin/env python
####################################################################################
#                                                                                  #
# Copyright (c) 2008 Dr. Conan C. Albrecht <conanATwarpDOTbyuDOTedu>               #
#                                                                                  #
# This file is part of Rurple.                                                     #
#                                                                                  #
# Rurple is free software; you can redistribute it and/or modify                   #
# it under the terms of the GNU General Public License as published by             #
# the Free Software Foundation; either version 2 of the License, or                #
# (at your option) any later version.                                              #
#                                                                                  #
# Rurple is distributed in the hope that it will be useful,                        #
# but WITHOUT ANY WARRANTY; without even the implied warranty of                   #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                    #
# GNU General Public License for more details.                                     #
#                                                                                  #
# You should have received a copy of the GNU General Public License                #
# along with Foobar; if not, write to the Free Software                            #
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA        #
#                                                                                  #
####################################################################################

####################################################################################
#
# Note: I wrote this script to wrap Rurple up with py2exe and py2app.  These
# two libraries allow Rurple to become a real .exe and OS X app bundle so
# people don't have to download Python or wxPython.  Thanks to Andre for creating
# the project.
#
# USAGE:
#   On Mac, you need py2app installed.  Run "./setup.sh" to create the bundle.
#           The new program will be in the dist/ directory.
#   On Windows, you need py2exe and InnoSetup installed .  Run "setup.bat" to
#           create the exe.
#

from distutils.core import setup
import glob, sys, os, os.path

# this manifest enables the standard Windows XP-looking theme
manifest = """
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1"
manifestVersion="1.0">
<assemblyIdentity
    version="0.64.1.0"
    processorArchitecture="x86"
    name="Controls"
    type="win32"
/>
<description>Picalo</description>
<dependency>
    <dependentAssembly>
        <assemblyIdentity
            type="win32"
            name="Microsoft.Windows.Common-Controls"
            version="6.0.0.0"
            processorArchitecture="X86"
            publicKeyToken="6595b64144ccf1df"
            language="*"
        />
    </dependentAssembly>
</dependency>
</assembly>
"""

# returns a list of all the files in a directory tree
def walk_dir(dirname):
  files = []
  ret = [ (dirname, files) ]
  for name in os.listdir(dirname):
    fullname = os.path.join(dirname, name)
    if os.path.isdir(fullname):
      ret.extend(walk_dir(fullname))
    else:
      files.append(fullname)
  return ret


# Generic options
options = {
  'name':             'RUR-PLE',
  'version':          '1.0.1',
  'description':      'A Python Learning Environment',
  'long_description': 'With the assistance of a robot named Reeborg, one can explore the fun of programming in the Python language.',
  'author':           'Andre Roberge',
  'author_email':     'http://code.google.com/p/rur-ple/',
  'url':              'http://code.google.com/p/rur-ple/',
  'packages':         [
                        'rur_py',
                      ],
  'scripts':          [
                        'rur_start.py',
                      ],
  'package_data':     {
                      },
  'data_files':       walk_dir('lessons') + \
                      walk_dir('python_files') + \
                      walk_dir('rur_images') + \
                      walk_dir('rur_programs') + \
                      walk_dir('rur_locale') + \
                      walk_dir('world_files'),
}

# windows specific
if len(sys.argv) >= 2 and sys.argv[1] == 'py2exe':
  try:
    import py2exe
  except ImportError:
    print 'Could not import py2exe.   Windows exe could not be built.'
    sys.exit(0)
  # windows-specific options
  options['windows'] = [
    {
      'script':'rur_start.py',
      'dest_base':'RUR-PLE',
      'icon_resources': [
        (1, 'rur_images/icon_win.ico' ),
       ],
      'other_resources': [
        (24, 1, manifest ),
      ],
    },
  ]
  options['options'] = {
    'py2exe': {
      'packages': [
        'rur_py',
      ],
#      'includes': '',
     }
  }


# mac specific
if len(sys.argv) >= 2 and sys.argv[1] == 'py2app':
  try:
    import py2app
  except ImportError:
    print 'Could not import py2app.   Mac bundle could not be built.'
    sys.exit(0)
  # mac-specific options
  options['app'] = ['rur_start.py']
  options['options'] = {
    'py2app': {
      'argv_emulation': True,
      'iconfile': 'rur_images/icon_mac.icns',
      'packages': [
      ],
#      'includes': '',
    }
  }


# run the setup
setup(**options)
