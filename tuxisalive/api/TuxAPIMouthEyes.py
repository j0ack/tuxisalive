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

class TuxAPIMouthEyes(object):
    """Class to control the movements of a body part (mouth or eyes).
    """
    
    def __init__(self, parent, positionStName, mvmRemStName, partName):
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
        # Body part field
        self.__positionStName = positionStName
        self.__mvmRemStName = mvmRemStName
        self.__partName = partName
        
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
    
    def open(self):
        """Open this body part.
        """
        cmd = "%s/open?" % self.__partName
        return self.__cmdSimpleResult(cmd)
    
    def close(self):
        """Close this body part.
        """
        cmd = "%s/close?" % self.__partName
        return self.__cmdSimpleResult(cmd)
    
    def off(self):
        """Stop the movement of this body part.
        """
        cmd = "%s/off?" % self.__partName
        return self.__cmdSimpleResult(cmd)
    
    def onAsync(self, count, finalState = SSV_NDEF):
        """Move this body part.
        (asynchronous)
        
        @param count: number of movements.
        @param finalState: requested state after the movement.
                            (SSV_NDEF|SSV_OPEN|SSV_CLOSE)
        @return: the success of the command.
        """
        if not checkValue(count, "int"):
            return False
        if not checkValue(finalState, "str"):
            return False
        if finalState not in SSV_MOUTHEYES_POSITIONS:
            return False
        cmd = "%s/on?count=%d&final_state=%s" % (self.__partName, 
                count, finalState)
        return self.__cmdSimpleResult(cmd)
    
    def on(self, count, finalState = SSV_NDEF):
        """Move this body part.
        
        @param count: number of movements.
        @param finalState: requested state after the movement.
                            (SSV_NDEF|SSV_OPEN|SSV_CLOSE)
        @return: the success of the command.
        """
        if not checkValue(count, "int"):
            return False
        if not checkValue(finalState, "str"):
            return False
        if finalState not in SSV_MOUTHEYES_POSITIONS:
            return False
        timeout = count * 1.0
        ret = self.onAsync(count, finalState)
        if self.__parent.server.getClientLevel() == CLIENT_LEVEL_ANONYME:
            return ret
        if ret:
            ret = self.waitMovingOff(timeout)
        return ret
    
    def onDuringAsync(self, duration, finalState = SSV_NDEF):
        """Move this body part during a number of seconds.
        (asynchronous)
        
        @param duration: duration time in seconds.
        @param finalState: requested state after the movement.
                            (SSV_NDEF|SSV_OPEN|SSV_CLOSE)
        @return: the success of the command.
        """
        if not checkValue(duration, "float"):
            return False
        if not checkValue(finalState, "str"):
            return False
        if finalState not in SSV_MOUTHEYES_POSITIONS:
            return False
        cmd = "%s/on_during?duration=%f&final_state=%s" % (self.__partName,
                    duration, finalState)
        return self.__cmdSimpleResult(cmd)
        
    def onDuring(self, duration, finalState = SSV_NDEF):
        """Move this body part during a number of seconds.
        
        @param duration: duration time in seconds.
        @param finalState: requested state after the movement.
                            (SSV_NDEF|SSV_OPEN|SSV_CLOSE)
        @return: the success of the command.
        """
        if not checkValue(duration, "float"):
            return False
        if not checkValue(finalState, "str"):
            return False
        if finalState not in SSV_MOUTHEYES_POSITIONS:
            return False
        timeout = 2.0 * duration
        ret = self.onDuringAsync(duration, finalState)
        if self.__parent.server.getClientLevel() == CLIENT_LEVEL_ANONYME:
            return ret
        if ret:
            ret = self.waitMovingOff(timeout)
        return ret
    
    def getPosition(self):
        """Get the position of the body part.
        
        @return: (SSV_NDEF|SSV_OPEN|SSV_CLOSE)
        """
        value, delay = self.__parent.status.requestOne(self.__positionStName)
        if value not in SSV_MOUTHEYES_POSITIONS:
            return SSV_NDEF
        else:
            return value
        
    def getMovingState(self):
        """Get the moving state of this body part.
        
        @return: a boolean.
        """
        value, delay = self.__parent.status.requestOne(self.__mvmRemStName)
        if value in [None, "0"]:
            return False
        else:
            return True
        
    def waitMovingOff(self, timeout):
        """Wait that this body part don't move.
        Not available for CLIENT_LEVEL_ANONYME level.
        
        @param timeout: maximal delay to wait.
        @return: the state of the wait result.
        """
        if self.__parent.server.getClientLevel() == CLIENT_LEVEL_ANONYME:
            raise TuxAPIExceptionCL, self.__parent.server.getClientLevel()
        return self.__parent.event.handler.waitCondition(self.__mvmRemStName, 
                            ("0", None), timeout)
        
    def waitPosition(self, position, timeout):
        """Wait a specific position of this body part.
        Not available for CLIENT_LEVEL_ANONYME level.
        
        @param position: position to wait.
        @param timeout: maximal delay to wait.
        @return: the state of the wait result.
        """
        if self.__parent.server.getClientLevel() == CLIENT_LEVEL_ANONYME:
            raise TuxAPIExceptionCL, self.__parent.server.getClientLevel()
        if position not in SSV_MOUTHEYES_POSITIONS:
            return False
        if self.getPosition() == position:
            return True
        return self.__parent.event.handler.waitCondition(self.__positionStName, 
                            (position, None), timeout)
