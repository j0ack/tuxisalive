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

from TuxAPIMisc import checkValue

class TuxAPIRawCommand(object):
    """Class to send a raw command to Tuxdroid.
    """
    
    def __init__(self, parent):
        """Constructor of the class.
        @param parent: parent object.
        @type parent: TuxAPI
        """
        # Parent field
        if str(type(parent)).find(".TuxAPI'") != -1:
            self.__parent = parent
            self.__eventHandlers = parent.getEventHandlers()
        else:
            self.__parent = None
            self.__eventHandlers = None
        
    def destroy(self):
        """Destructor of the class.
        """
        pass
    
    def __cmdSimpleResult(self, cmd):
        """
        """
        if self.__eventHandlers != None:
            if self.__parent != None:
                # Request
                if self.__parent.server.request(cmd, {}, {}):
                    return True
        return False
    
    def send(self, b0, b1, b2, b3, b4):
        """
        """
        if not checkValue(b0, "int"):
            return False
        if not checkValue(b1, "int"):
            return False
        if not checkValue(b2, "int"):
            return False
        if not checkValue(b3, "int"):
            return False
        if not checkValue(b4, "int"):
            return False
        cmd = "macro/play?macro=0.0:RAW_CMD:0x%.2x:0x%.2x:0x%.2x:0x%.2x:0x%.2x" % (
                    b0, b1, b2, b3, b4)
        
        return self.__cmdSimpleResult(cmd)
    