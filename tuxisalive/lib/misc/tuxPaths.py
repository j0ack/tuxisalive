# -*- coding: latin1 -*-

import version
__author__ = version.author
__date__ = version.date
__version__ = version.version
__licence__ = version.licence
del version

#    Copyright (C) 2008 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

import os

TUXDROID_BASE_PATH = None
TUXDROID_LANGUAGE = None
TUXDROID_DEFAULT_LOCUTOR = None
USER_BASE_PATH = None

def __getDefaultLocutor(isoLang):
    """Fill the default locutor for a iso lang.
    """
    global TUXDROID_DEFAULT_LOCUTOR
    
    if isoLang == "ar":
        TUXDROID_DEFAULT_LOCUTOR = "Salma8k"
    elif isoLang == "en_GB":
        TUXDROID_DEFAULT_LOCUTOR = "Graham8k"
    elif isoLang == "da":
        TUXDROID_DEFAULT_LOCUTOR = "Mette8k"
    elif isoLang == "nl":
        TUXDROID_DEFAULT_LOCUTOR = "Femke8k"
    elif isoLang == "de":
        TUXDROID_DEFAULT_LOCUTOR = "Klaus8k"
    elif isoLang == "no":
        TUXDROID_DEFAULT_LOCUTOR = "Kari8k"
    elif isoLang == "pt":
        TUXDROID_DEFAULT_LOCUTOR = "Celia8k"
    elif isoLang == "sv":
        TUXDROID_DEFAULT_LOCUTOR = "Erik8k"
    elif isoLang == "fr":
        TUXDROID_DEFAULT_LOCUTOR = "Bruno8k"
    elif isoLang == "en_US":
        TUXDROID_DEFAULT_LOCUTOR = "Ryan8k"
    elif isoLang == "nl_BE":
        TUXDROID_DEFAULT_LOCUTOR = "Sofie8k"
    elif isoLang == "it":
        TUXDROID_DEFAULT_LOCUTOR = "Chiara8k"
    elif isoLang == "es":
        TUXDROID_DEFAULT_LOCUTOR = "Maria8k"
    else:
        TUXDROID_DEFAULT_LOCUTOR = "Ryan8k"

if os.name == 'nt':
    from _winreg import *
    aReg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    aKey = OpenKey(aReg, r"SOFTWARE\Tuxdroid\TuxdroidSetup")
    TUXDROID_BASE_PATH = QueryValueEx(aKey, "Install_Dir")[0]
    TUXDROID_LANGUAGE = QueryValueEx(aKey, "Language")[0]
    CloseKey(aReg)
    __getDefaultLocutor(TUXDROID_LANGUAGE)
else:
    TUXDROID_LANGUAGE = "en_US"
    __getDefaultLocutor(TUXDROID_LANGUAGE)
    if os.path.isfile("/etc/tuxdroid/tuxdroid.conf"):
        try:
            f = open("/etc/tuxdroid/tuxdroid.conf", 'rb')
            stream = f.read()
            lines = stream.split('\n')
            for line in lines:
                if line.find('PREFIX=') != -1:
                    prefix = line[7:]
                    TUXDROID_BASE_PATH = os.path.join(prefix, 'share/tuxdroid')
            f.close()
        except:
            TUXDROID_BASE_PATH = "/usr/share/tuxdroid"
USER_BASE_PATH = os.path.expanduser("~")       