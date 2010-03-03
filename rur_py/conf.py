# -*- coding: utf-8
""" RUR-PLE: Roberge's Used Robot - a Python Learning Environment
    conf.py - contains various application and user properties and some
    methods for saving and loading configuraton data.
    Version 1.0
    Author: Andre Roberge    Copyright  2006
    andre.roberge@gmail.com
"""
import sys
import os
import shutil
import tempfile
import ConfigParser
import locale

_Settings = None

def getSettings():
    '''Creates and returns a class with properties pointing
    to some basic application and user locations.
     @return (Settings): the Settings class as "singleton".
    '''
    global _Settings

    if _Settings != None:
        return _Settings

    props = {}

    #--- top level application directory
    callingRule = "First call of getSettings() has to occur " \
        "in rur-ple's top level directory"
    assert "rur_start.py" in os.listdir('.'), callingRule
    APP_HOME = os.path.abspath('.')
    props['APP_HOME'] = APP_HOME

    # images for program - excluding lessons
    props['IMAGE_DIR'] = os.path.join(APP_HOME, "rur_images")

    # sounds for program - excluding lessons
    props['SOUNDS_DIR'] = os.path.join(APP_HOME, "sounds")

    # sample programs
    sample_progs_dir = os.path.join(APP_HOME, "rur_programs")
    props['SAMPLE_PROGS_DIR'] = sample_progs_dir

    # sample worlds
    sample_worlds_dir = os.path.join(APP_HOME, "world_files")
    props['SAMPLE_WORLDS_DIR'] = sample_worlds_dir

    # translation files
    props['LOCALE_DIR'] = os.path.join(APP_HOME, "rur_locale")

    # lessons
    props['LESSONS_DIR'] = os.path.join(APP_HOME, "lessons")

    # SCREEN defaults depend on wx, therefore set to None here.
    props['SCREEN'] = None

    #--- top level user directory
    userDir = getUserDir()
    props['USER_DIR'] = userDir

    #--- user configuration file
    props['USER_CFG'] = "user.cfg"

    # predefined programs
    user_progs_dir = os.path.join(userDir, 'programs')
    props['USER_PROGS_DIR'] = user_progs_dir
    if tryCreate(user_progs_dir):
        shutil.copytree(sample_progs_dir,
            os.path.join(user_progs_dir, 'samples'))
   
    # predefined worlds
    user_worlds_dir = os.path.join(userDir, 'worlds')
    props['USER_WORLDS_DIR'] = user_worlds_dir
    if tryCreate(user_worlds_dir):
        shutil.copytree(sample_worlds_dir,
            os.path.join(user_worlds_dir, 'samples'))

    # create configuration file

    # create and return a class as "singleton"
    _Settings = type('Settings',(), props)
    return _Settings

def getUserDir():
    '''Returns the user directory, i.e. the place where user specific
    data are stored.
     @return (str): the platform dependent user directory.
    '''
    platform = sys.platform

    userdir = ''
    if platform in ('linux2', 'darwin', 'cygwin') or os.name == 'posix':
        home = os.path.expanduser('~')
        if home != '~':
            userdir = os.path.join(home, '.config', 'rurple')
    elif platform == 'win32':
        if 'APPDATA' in  os.environ:
            userdir = os.path.join(os.environ['APPDATA'], 'rurple')

    if userdir == '':
        userdir =  os.path.join(tempfile.gettempdir(), 'rurple')

    return userdir

def tryCreate(adir):
    '''Tries to create path aDir.
    @param aDir (str) : name of directory to create
    @return (bool): true if succeeded else false.
    '''
    success = False
    if not os.path.exists(adir):
        try:
            os.makedirs(adir)
            success = True
        except OSError:
            print _("directory for user data %s cannot be created.") % adir
            
    return success

def getLanguage():
    '''Get 2-letter language code from user configuration file.
     @return (str): language code if succeeded else default ('en').
    '''
    storage = _getStorage(getSettings().USER_CFG)
    langCode = storage.get("locale", "lang")
    return langCode

def setLanguage(langCode):
    '''Write 2-letter language code from user configuration file.
    @param langCode (str) : new language code.
    @return (bool): true if succeeded else false.
    '''
    fileName = getSettings().USER_CFG
    storage = _getStorage(fileName)
    success = storage.set("locale", "lang", langCode)
    _saveStorage(storage, fileName)
    return success

def getLessonsNlDir():
    '''Retrieve path to lessons in current natural language.
    @return (str): path to lessons in current natural language.
    '''
    # lessons and other html files (language dependent)
    return os.path.join(getSettings().APP_HOME, "lessons", getLanguage())

def getAvailableLanguages():
    '''Retrieve available languages from directories under rur_locale.
    @return (set): set of available languages.
    '''
    for d, sd, sf in os.walk(getSettings().LOCALE_DIR):
        return [lang for lang in sd if lang[0] != '.']

def _getStorage(fileName):
    '''Creates a RawConfigParser object from the given file (ini format).
    @param fileName (str) : name of file to load from.
    @return (RawConfigParser): theRawConfigParser object
    '''
    cp = ConfigParser.RawConfigParser()
    try:
        path = os.path.join(getSettings().USER_DIR, fileName)
        if os.path.exists(path):
            f = open(path)
            cp.readfp(f)
            f.close()
        else:
            cp = _defaultStorage(fileName)
        return cp
    except IOError:
        return None

def _saveStorage(cp, fileName):
    '''Saves a RawConfigParser object to the given file.
    @param cp (RawConfigParser): theRawConfigParser object to save.
    @param fileName (str) : name of file to save to.
    @return (bool): success status of the operation.
    '''
    try:
        path = os.path.join(getSettings().USER_DIR, fileName)
        f = open(path, 'w')
        cp.write(f)
        f.close()
        return True
    except IOError:
        return False

def _defaultStorage(fileName):
    '''Creates a RawConfigParser object with default settings and saves it to
    thr given file. The file is created if it doesn't exist.
    @param fileName (str) : name of file to load from.
    @return (RawConfigParser): the RawConfigParser object
    '''
    try:
        cp = ConfigParser.RawConfigParser()
        cp.add_section('locale')
        cp.set('locale', 'lang', _getDefaultLanguage())
        path = os.path.join(getSettings().USER_DIR, fileName)
        f = open(path, 'w')
        cp.write(f)
        f.close()
        return cp
    except IOError:
        return None

def _getDefaultLanguage():
    '''Guesses the default language from the environment settings of the user.
    @return (str): the 2-letter code of the default language.
    '''
    try:
        defaultLanguage = locale.getdefaultlocale()[0].split('_')[0]
        if not defaultLanguage in getAvailableLanguages():
            defaultLanguage = 'en'
    except Exception:
        defaultLanguage = 'en'

    return defaultLanguage
