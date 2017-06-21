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

from TuxAPIMisc import checkValue
from TuxAPIConst import *
from TuxAPIExceptionCL import TuxAPIExceptionCL

class TuxAPIDongleRadio(object):
    """Class to interact with the connection/disconnection of the radio/dongle.
    """
    
    def __init__(self, parent, stStName):
        """Constructor of the class.
        @param parent: parent object.
        @type parent: TuxAPI
        """
        self.__stStName = stStName
        # Parent field
        if str(type(parent)).find(".TuxAPI'") != -1:
            self.__parent = parent
            self.__eventHandlers = parent.getEventHandlers()
            self.__eventHandler = self.__eventHandlers.getEventHandler(self.__stStName)
        else:
            self.__parent = None
            self.__eventHandlers = None
            self.__eventHandler = None
            
    def destroy(self):
        """Destructor of the class.
        """
        pass
            
    def getConnected(self):
        """Return the state of the radio/dongle connection.
        """
        if self.__parent != None:
            value, delay = self.__parent.status.requestOne(self.__stStName)
            if value != None:
                return eval(value)
        return False
        
    def waitConnected(self, timeout):
        """Wait until the radio/dongle was connected.
        Not available for CLIENT_LEVEL_ANONYME level.
        
        @param timeout: maximal delay to wait.
        @return: the state of the wait result.
        """
        if self.__parent.server.getClientLevel() == CLIENT_LEVEL_ANONYME:
            raise TuxAPIExceptionCL, self.__parent.server.getClientLevel()
        if not checkValue(timeout, "float"):
            return False
        if self.getConnected():
            return True
        if self.__parent != None:
            return self.__eventHandler.waitCondition(("True", None), timeout)
        return False
    
    def waitDisconnected(self, timeout):
        """Wait until the radio/dongle was disconnected.
        Not available for CLIENT_LEVEL_ANONYME level.
        
        @param timeout: maximal delay to wait.
        @return: the state of the wait result.
        """
        if self.__parent.server.getClientLevel() == CLIENT_LEVEL_ANONYME:
            raise TuxAPIExceptionCL, self.__parent.server.getClientLevel()
        if not checkValue(timeout, "float"):
            return False
        if not self.getConnected():
            return True
        if self.__parent != None:
            return self.__eventHandler.waitCondition(("False", None), timeout)
        return False
    
    def registerEventOnConnected(self, funct, idx = None):
        """Register a callback on the connected event.
        Not available for CLIENT_LEVEL_ANONYME level.
        
        @param funct: pointer to the function.
        @param idx: index from a previous register.
        @return: the new index of the callback in the handler.
        """
        if self.__parent.server.getClientLevel() == CLIENT_LEVEL_ANONYME:
            raise TuxAPIExceptionCL, self.__parent.server.getClientLevel()
        nIdx = -1
        if self.__eventHandler != None:
            nIdx = self.__eventHandler.register(funct, ("True", None), idx)
        return nIdx
    
    def unregisterEventOnConnected(self, idx):
        """Unregister a callback from the connected event.
        Not available for CLIENT_LEVEL_ANONYME level.
        
        @param idx: index from a previous register.
        """
        if self.__parent.server.getClientLevel() == CLIENT_LEVEL_ANONYME:
            raise TuxAPIExceptionCL, self.__parent.server.getClientLevel()
        if self.__eventHandler != None:
            self.__eventHandler.unregister(idx)
            
    def registerEventOnDisconnected(self, funct, idx = None):
        """Register a callback on the disconnected event.
        Not available for CLIENT_LEVEL_ANONYME level.
        
        @param funct: pointer to the function.
        @param idx: index from a previous register.
        @return: the new index of the callback in the handler.
        """
        if self.__parent.server.getClientLevel() == CLIENT_LEVEL_ANONYME:
            raise TuxAPIExceptionCL, self.__parent.server.getClientLevel()
        nIdx = -1
        if self.__eventHandler != None:
            nIdx = self.__eventHandler.register(funct, ("False", None), idx)
        return nIdx
    
    def unregisterEventOnDisconnected(self, idx):
        """Unregister a callback from the disconnected event.
        Not available for CLIENT_LEVEL_ANONYME level.
        
        @param idx: index from a previous register.
        """
        if self.__parent.server.getClientLevel() == CLIENT_LEVEL_ANONYME:
            raise TuxAPIExceptionCL, self.__parent.server.getClientLevel()
        if self.__eventHandler != None:
            self.__eventHandler.unregister(idx)