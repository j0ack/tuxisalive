# -*- coding: latin1 -*-

"""
Tux shell
=========
Tux shell is the shell way to use Tuxdroid. It create an API object with the
"Free" client mode.
"""

from tuxisalive.api.version import author, date, version, licence
__author__ = author
__date__ = date
__version__ = version
__licence__ = licence
del author, date, version, licence

#    Copyright (C) 2008 C2ME Sa
#    Rémi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

import sys
import signal
import atexit
import os

from tuxisalive.api.TuxAPIConst import *
from tuxisalive.api.TuxAPI import TuxAPI

global tux

tux = TuxAPI("127.0.0.1", 270)

verString = tux.getVersion()
verH = "".join("=" * len(verString))
print verH
print verString
print verH

if os.name != 'nt':
    if not 'readline' in sys.modules:
        print "For interctive use, run: python -i sh.py"
        sys.exit(0)

tux.server.autoConnect(CLIENT_LEVEL_FREE, "TuxShell", "NoPasswd")
tux.tts.isConsole()

def sigExit(signum, frame):
    sys.exit(signum)
    
def exit():
    tux.destroy()
    sys.exit(0)

def myExitFunct():
    tux.destroy()

signal.signal(signal.SIGTERM, sigExit)
signal.signal(signal.SIGINT, sigExit)
atexit.register(myExitFunct)
