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

class TuxAPIFlippers(object):
    """Class to control the flippers movements.
    """
    
    def __init__(self, parent):
        """Constructor of the class.
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
        if self.__parent != None:
            # Request
            if self.__parent.server.request(cmd, {}, {}):
                return True
        return False
    
    def __checkSpeed(self, speed):
        """
        """
        if speed < SPV_VERYSLOW:
            speed = SPV_VERYSLOW
        elif speed > SPV_VERYFAST:
            speed = SPV_VERYFAST
        return speed
    
    def up(self):
        """Set the flippers to up.
        """
        cmd = "flippers/up?"
        return self.__cmdSimpleResult(cmd)
    
    def down(self):
        """Set the flippers to down.
        """
        cmd = "flippers/down?"
        return self.__cmdSimpleResult(cmd)
    
    def off(self):
        """Stop the flippers movement.
        """
        cmd = "flippers/off?"
        return self.__cmdSimpleResult(cmd)
    
    def setSpeed(self, speed):
        """Set the speed of the flippers movement.
        
        @param speed: speed of the rotation.
        (SPV_VERYSLOW|SPV_SLOW|SPV_NORMAL|SPV_FAST|SPV_VERYFAST)
        @return: the success of the command.
        """
        if not checkValue(speed, "int"):
            return False
        speed = self.__checkSpeed(speed)
        cmd = "flippers/speed?value=%d" % speed
        return self.__cmdSimpleResult(cmd)
    
    def onAsync(self, count, finalState = SSV_UP, speed = SPV_VERYFAST):
        """Move the flippers. (asynchronous)
        
        
        @param count: number of movements.
        @param finalState: requested state after the movement.
                            (SSV_NDEF|SSV_UP|SSV_DOWN)
        @param speed: speed of the rotation.
        (SPV_VERYSLOW|SPV_SLOW|SPV_NORMAL|SPV_FAST|SPV_VERYFAST)
        @return: the success of the command.
        """
        if not checkValue(count, "int"):
            return False
        if not checkValue(finalState, "str"):
            return False
        if finalState not in SSV_FLIPPERS_POSITIONS:
            return False
        cmd = "flippers/on?count=%d&final_state=%s" % (count, finalState)
        ret = self.__cmdSimpleResult(cmd)
        if ret:
            ret = self.setSpeed(speed)
        return ret
    
    def on(self, count, finalState = SSV_UP, speed = SPV_VERYFAST):
        """Move the flippers.
        
        @param count: number of movements.
        @param finalState: requested state after the movement.
                            (SSV_NDEF|SSV_UP|SSV_DOWN)
        @param speed: speed of the movement.
        (SPV_VERYSLOW|SPV_SLOW|SPV_NORMAL|SPV_FAST|SPV_VERYFAST)
        @return: the success of the command.
        """
        if not checkValue(count, "int"):
            return False
        if not checkValue(finalState, "str"):
            return False
        if finalState not in SSV_FLIPPERS_POSITIONS:
            return False
        timeout = count * 1.0
        ret = self.onAsync(count, finalState, speed)
        if self.__parent.server.getClientLevel() == CLIENT_LEVEL_ANONYME:
            return ret
        if ret:
            ret = self.waitMovingOff(timeout)
        return ret
    
    def onDuringAsync(self, duration, finalState = SSV_UP, speed = SPV_VERYFAST):
        """Move the flippers during a number of seconds.
        (asynchronous)
        
        @param duration: duration time in seconds.
        @param finalState: requested state after the movement.
                            (SSV_NDEF|SSV_UP|SSV_DOWN)
        @param speed: speed of the rotation.
        (SPV_VERYSLOW|SPV_SLOW|SPV_NORMAL|SPV_FAST|SPV_VERYFAST)
        @return: the success of the command.
        """
        if not checkValue(duration, "float"):
            return False
        if not checkValue(finalState, "str"):
            return False
        if finalState not in SSV_FLIPPERS_POSITIONS:
            return False
        cmd = "flippers/on_during?duration=%f&final_state=%s" % (duration, finalState)
        ret = self.__cmdSimpleResult(cmd)
        if ret:
            ret = self.setSpeed(speed)
        return ret
        
    def onDuring(self, duration, finalState = SSV_UP, speed = SPV_VERYFAST):
        """Move the flippers during a number of seconds.
        
        @param duration: duration time in seconds.
        @param finalState: requested state after the movement.
                            (SSV_NDEF|SSV_UP|SSV_DOWN)
        @param speed: speed of the movement.
        (SPV_VERYSLOW|SPV_SLOW|SPV_NORMAL|SPV_FAST|SPV_VERYFAST)
        @return: the success of the command.
        """
        if not checkValue(duration, "float"):
            return False
        if not checkValue(finalState, "str"):
            return False
        if finalState not in SSV_FLIPPERS_POSITIONS:
            return False
        timeout = 2.0 * duration
        ret = self.onDuringAsync(duration, finalState, speed)
        if self.__parent.server.getClientLevel() == CLIENT_LEVEL_ANONYME:
            return ret
        if ret:
            ret = self.waitMovingOff(timeout)
        return ret
    
    def getPosition(self):
        """Get the position of the flippers.
        
        @return: (SSV_NDEF|SSV_UP|SSV_DOWN)
        """
        value, delay = self.__parent.status.requestOne(ST_NAME_FLIPPERS_POSITION)
        if value not in SSV_FLIPPERS_POSITIONS:
            return SSV_NDEF
        else:
            return value
        
    def getMovingState(self):
        """Get the moving state of the flippers.
        
        @return: a boolean.
        """
        value, delay = self.__parent.status.requestOne(ST_NAME_FLIPPERS_MOTOR_ON)
        if value in [None, "False"]:
            return False
        else:
            return True
        
    def waitMovingOff(self, timeout):
        """Wait that the flippers don't move.
        Not available for CLIENT_LEVEL_ANONYME level.
        
        @param timeout: maximal delay to wait.
        @return: the state of the wait result.
        """
        if self.__parent.server.getClientLevel() == CLIENT_LEVEL_ANONYME:
            raise TuxAPIExceptionCL, self.__parent.server.getClientLevel()
        return self.__parent.event.handler.waitCondition(ST_NAME_FLIPPERS_MOTOR_ON, 
                            ("False", None), timeout)
        
    def waitPosition(self, position, timeout):
        """Wait a specific position of the flippers.
        Not available for CLIENT_LEVEL_ANONYME level.
        
        @param timeout: maximal delay to wait.
        @return: the state of the wait result.
        """
        if self.__parent.server.getClientLevel() == CLIENT_LEVEL_ANONYME:
            raise TuxAPIExceptionCL, self.__parent.server.getClientLevel()
        if position not in SSV_FLIPPERS_POSITIONS:
            return False
        if self.getPosition() == position:
            return True
        return self.__parent.event.handler.waitCondition(ST_NAME_FLIPPERS_POSITION, 
                            (position, None), timeout)
