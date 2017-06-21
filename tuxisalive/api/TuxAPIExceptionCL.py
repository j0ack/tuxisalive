# -*- coding: latin1 -*-

import version
__author__ = version.author
__date__ = version.date
__version__ = version.version
__licence__ = version.licence
del version

#    Copyright (C) 2008 C2ME Sa
#    Rémi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

from TuxAPIConst import *

class TuxAPIExceptionCL(Exception):
    
    def __init__(self, value):
        idx = CLIENT_LEVELS.index(value)
        self.value = CLIENT_LEVELS_NAME[idx]
        
    def __str__(self):
        strRes = "\n---------------------------------------------------------------------------"
        strRes += "\nThis functionality is not allowed for the client level (%s)" % self.value
        strRes += "\n---------------------------------------------------------------------------"
        return strRes
