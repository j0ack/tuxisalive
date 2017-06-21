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

class TuxAPIButton(object):
    """Class to control the buttons.
    """
    
    def __init__(self, parent):
        """Constructor of the class.
        @param parent: parent object.
        @type parent: TuxAPI
        """
        self.left = TuxAPISwitch(parent, ST_NAME_LEFT_BUTTON)
        """Left flipper switch. 
        @see: TuxAPISwitch
        """
        self.right = TuxAPISwitch(parent, ST_NAME_RIGHT_BUTTON)
        """Right flipper switch. 
        @see: TuxAPISwitch
        """
        self.head = TuxAPISwitch(parent, ST_NAME_HEAD_BUTTON)
        """Head switch. 
        @see: TuxAPISwitch
        """
        self.remote = TuxAPIRemote(parent)
        """Remote.
        @see: TuxAPIRemote
        """
        
    def destroy(self):
        """Destructor of the class.
        """
        pass
        
class TuxAPISwitch(object):
    """Class to control the state of a switch.
    """
    
    def __init__(self, parent, switchStName):
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
        # Switch field
        self.__switchStName = switchStName
        
    def destroy(self):
        """Destructor of the class.
        """
        pass
    
    def getState(self):
        """Return the state of the switch.
        """
        if self.__parent != None:
            value, delay = self.__parent.status.requestOne(self.__switchStName)
            if value != None:
                return eval(value)
        return False
    
    def waitPressed(self, timeout):
        """Wait until the switch was pressed.
        Not available for CLIENT_LEVEL_ANONYME level.
        
        @param timeout: maximal delay to wait.
        @return: the state of the wait result.
        """
        if self.__parent.server.getClientLevel() == CLIENT_LEVEL_ANONYME:
            raise TuxAPIExceptionCL, self.__parent.server.getClientLevel()
        if not checkValue(timeout, "float"):
            return False
        if self.getState():
            return True
        if self.__parent != None:
            return self.__eventHandlers.waitCondition(self.__switchStName, ("True", None), 
                                                      timeout)
        return False
    
    def waitReleased(self, timeout):
        """Wait until the switch was released.
        Not available for CLIENT_LEVEL_ANONYME level.
        
        @param timeout: maximal delay to wait.
        @return: the state of the wait result.
        """
        if self.__parent.server.getClientLevel() == CLIENT_LEVEL_ANONYME:
            raise TuxAPIExceptionCL, self.__parent.server.getClientLevel()
        if not checkValue(timeout, "float"):
            return False
        if not self.getState():
            return True
        if self.__parent != None:
            return self.__eventHandlers.waitCondition(self.__switchStName, ("False", None), 
                                                      timeout)
        return False
    
    def registerEventOnPressed(self, funct, idx = None):
        """Register a callback on the pressed event.
        Not available for CLIENT_LEVEL_ANONYME level.
        
        @param funct: pointer to the function.
        @param idx: index from a previous register.
        @return: the new index of the callback in the handler.
        """
        if self.__parent.server.getClientLevel() == CLIENT_LEVEL_ANONYME:
            raise TuxAPIExceptionCL, self.__parent.server.getClientLevel()
        nIdx = -1
        if self.__eventHandlers != None:
            nIdx = self.__eventHandlers.register(self.__switchStName, funct, ("True", None), idx)
        return nIdx
    
    def unregisterEventOnPressed(self, idx):
        """Unregister a callback from the pressed event.
        Not available for CLIENT_LEVEL_ANONYME level.
        
        @param idx: index from a previous register.
        """
        if self.__parent.server.getClientLevel() == CLIENT_LEVEL_ANONYME:
            raise TuxAPIExceptionCL, self.__parent.server.getClientLevel()
        if self.__eventHandlers != None:
            self.__eventHandlers.unregister(self.__switchStName, idx)
            
    def registerEventOnReleased(self, funct, idx = None):
        """Register a callback on the pressed event.
        Not available for CLIENT_LEVEL_ANONYME level.
        
        @param funct: pointer to the function.
        @param idx: index from a previous register.
        @return: the new index of the callback in the handler.
        """
        if self.__parent.server.getClientLevel() == CLIENT_LEVEL_ANONYME:
            raise TuxAPIExceptionCL, self.__parent.server.getClientLevel()
        nIdx = -1
        if self.__eventHandlers != None:
            nIdx = self.__eventHandlers.register(self.__switchStName, funct, ("False", None), idx)
        return nIdx
    
    def unregisterEventOnReleased(self, idx):
        """Unregister a callback from the pressed event.
        Not available for CLIENT_LEVEL_ANONYME level.
        
        @param idx: index from a previous register.
        """
        if self.__parent.server.getClientLevel() == CLIENT_LEVEL_ANONYME:
            raise TuxAPIExceptionCL, self.__parent.server.getClientLevel()
        if self.__eventHandlers != None:
            self.__eventHandlers.unregister(self.__switchStName, idx)
            
class TuxAPIRemote(object):
    """Class the control the state of the remote.
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
    
    def getState(self):
        """Return the state of the switch.
        """
        if self.__parent != None:
            value, delay = self.__parent.status.requestOne(ST_NAME_REMOTE_BUTTON)
            return value
        return K_RELEASED
    
    def waitPressed(self, timeout, key):
        """Wait until the remote was pressed.
        Not available for CLIENT_LEVEL_ANONYME level.
        
        @param timeout: maximal delay to wait.
        @param key: key to wiat.
        @return: the state of the wait result.
        """
        if self.__parent.server.getClientLevel() == CLIENT_LEVEL_ANONYME:
            raise TuxAPIExceptionCL, self.__parent.server.getClientLevel()
        if not checkValue(timeout, "float"):
            return False
        if not key in REMOTE_KEY_LIST:
            return False
        if self.getState() == key:
            return True
        if self.__parent != None:
            return self.__eventHandlers.waitCondition(ST_NAME_REMOTE_BUTTON, 
                                                      (key, None), 
                                                      timeout)
        return False
    
    def waitReleased(self, timeout):
        """Wait until the remote was released.
        Not available for CLIENT_LEVEL_ANONYME level.
        
        @param timeout: maximal delay to wait.
        @return: the state of the wait result.
        """
        if self.__parent.server.getClientLevel() == CLIENT_LEVEL_ANONYME:
            raise TuxAPIExceptionCL, self.__parent.server.getClientLevel()
        if not checkValue(timeout, "float"):
            return False
        if self.getState() == K_RELEASED:
            return True
        if self.__parent != None:
            return self.__eventHandlers.waitCondition(ST_NAME_REMOTE_BUTTON, 
                                                      (K_RELEASED, None), 
                                                      timeout)
        return False
    
    def registerEventOnPressed(self, funct, key, idx = None):
        """Register a callback on the pressed event.
        Not available for CLIENT_LEVEL_ANONYME level.
        
        @param funct: pointer to the function.
        @param idx: index from a previous register.
        @param key: remote key.
        @return: the new index of the callback in the handler.
        """
        if self.__parent.server.getClientLevel() == CLIENT_LEVEL_ANONYME:
            raise TuxAPIExceptionCL, self.__parent.server.getClientLevel()
        nIdx = -1
        if self.__eventHandlers != None:
            nIdx = self.__eventHandlers.register(ST_NAME_REMOTE_BUTTON, funct, 
                                                 (key, None), idx)
        return nIdx
    
    def unregisterEventOnPressed(self, idx):
        """Unregister a callback from the pressed event.
        Not available for CLIENT_LEVEL_ANONYME level.
        
        @param idx: index from a previous register.
        """
        if self.__parent.server.getClientLevel() == CLIENT_LEVEL_ANONYME:
            raise TuxAPIExceptionCL, self.__parent.server.getClientLevel()
        if self.__eventHandlers != None:
            self.__eventHandlers.unregister(ST_NAME_REMOTE_BUTTON, idx)
            
    def registerEventOnReleased(self, funct, idx = None):
        """Register a callback on the released event.
        Not available for CLIENT_LEVEL_ANONYME level.
        
        @param funct: pointer to the function.
        @param idx: index from a previous register.
        @return: the new index of the callback in the handler.
        """
        if self.__parent.server.getClientLevel() == CLIENT_LEVEL_ANONYME:
            raise TuxAPIExceptionCL, self.__parent.server.getClientLevel()
        nIdx = -1
        if self.__eventHandlers != None:
            nIdx = self.__eventHandlers.register(ST_NAME_REMOTE_BUTTON, funct, 
                                                 (K_RELEASED, None), idx)
        return nIdx
    
    def unregisterEventOnReleased(self, idx):
        """Unregister a callback from the released event.
        Not available for CLIENT_LEVEL_ANONYME level.
        
        @param idx: index from a previous register.
        """
        if self.__parent.server.getClientLevel() == CLIENT_LEVEL_ANONYME:
            raise TuxAPIExceptionCL, self.__parent.server.getClientLevel()
        if self.__eventHandlers != None:
            self.__eventHandlers.unregister(ST_NAME_REMOTE_BUTTON, idx)