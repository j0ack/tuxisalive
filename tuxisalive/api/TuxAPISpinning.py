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

class TuxAPISpinning(object):
    """Class to control the spinning movements.
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
    
    def setSpeed(self, speed):
        """Set the speed of rotation.
        
        @param speed: speed of the rotation.
        (SPV_VERYSLOW|SPV_SLOW|SPV_NORMAL|SPV_FAST|SPV_VERYFAST)
        @return: the success of the command.
        """
        if not checkValue(speed, "int"):
            return False
        speed = self.__checkSpeed(speed)
        cmd = "spinning/speed?value=%d" % speed
        return self.__cmdSimpleResult(cmd)
    
    def off(self):
        """Stop the spinning movement.
        
        @return: the success of the command.
        """
        cmd = "spinning/off?"
        return self.__cmdSimpleResult(cmd)
    
    def leftOnAsync(self, turns, speed = SPV_VERYFAST):
        """Move the robot to the left. (asynchronous)
        
        @param turns: number of turns.
        @param speed: speed of the rotation.
        (SPV_VERYSLOW|SPV_SLOW|SPV_NORMAL|SPV_FAST|SPV_VERYFAST)
        @return: the success of the command.
        """
        if not checkValue(turns, "float"):
            return False
        count = int(turns * 4)
        if (count == 0):
            count = 1
        if (count > 255):
            count = 255
        cmd = "spinning/left_on?count=%d" % count
        ret = self.__cmdSimpleResult(cmd)
        if ret:
            ret = self.setSpeed(speed)
        return ret
    
    def rightOnAsync(self, turns, speed = SPV_VERYFAST):
        """Move the robot to the right. (asynchronous)
        
        @param turns: number of turns.
        @param speed: speed of the rotation.
        (SPV_VERYSLOW|SPV_SLOW|SPV_NORMAL|SPV_FAST|SPV_VERYFAST)
        @return: the success of the command.
        """
        if not checkValue(turns, "float"):
            return False
        count = int(turns * 4)
        if (count == 0):
            count = 1
        if (count > 255):
            count = 255
        cmd = "spinning/right_on?count=%d" % count
        ret = self.__cmdSimpleResult(cmd)
        if ret:
            ret = self.setSpeed(speed)
        return ret
    
    def leftOn(self, turns, speed = SPV_VERYFAST):
        """Move the robot to the left.
        
        @param turns: number of turns.
        @param speed: speed of the rotation.
        (SPV_VERYSLOW|SPV_SLOW|SPV_NORMAL|SPV_FAST|SPV_VERYFAST)
        @return: the success of the command.
        """
        
        timeout = turns * 5.0
        ret = self.leftOnAsync(turns, speed)
        if self.__parent.server.getClientLevel() == CLIENT_LEVEL_ANONYME:
            return ret
        if ret:
            ret = self.waitLeftMovingOff(timeout)
        return ret
    
    def rightOn(self, turns, speed = SPV_VERYFAST):
        """Move the robot to the right.
        
        @param turns: number of turns.
        @param speed: speed of the rotation.
        (SPV_VERYSLOW|SPV_SLOW|SPV_NORMAL|SPV_FAST|SPV_VERYFAST)
        @return: the success of the command.
        """
        
        timeout = turns * 5.0
        ret = self.rightOnAsync(turns, speed)
        if self.__parent.server.getClientLevel() == CLIENT_LEVEL_ANONYME:
            return ret
        if ret:
            ret = self.waitRightMovingOff(timeout)
        return ret
    
    def leftOnDuringAsync(self, duration, speed = SPV_VERYFAST):
        """Move the robot to the left during a number of seconds. 
        (asynchronous)
        
        @param duration: duration of the rotation.
        @param speed: speed of the rotation.
        (SPV_VERYSLOW|SPV_SLOW|SPV_NORMAL|SPV_FAST|SPV_VERYFAST)
        @return: the success of the command.
        """
        if not checkValue(duration, "float"):
            return False
        cmd = "spinning/left_on_during?duration=%f" % duration
        ret = self.__cmdSimpleResult(cmd)
        if ret:
            ret = self.setSpeed(speed)
        return ret
    
    def rightOnDuringAsync(self, duration, speed = SPV_VERYFAST):
        """Move the robot to the right during a number of seconds. 
        (asynchronous)
        
        @param duration: duration of the rotation.
        @param speed: speed of the rotation.
        (SPV_VERYSLOW|SPV_SLOW|SPV_NORMAL|SPV_FAST|SPV_VERYFAST)
        @return: the success of the command.
        """
        if not checkValue(duration, "float"):
            return False
        cmd = "spinning/right_on_during?duration=%f" % duration
        ret = self.__cmdSimpleResult(cmd)
        if ret:
            ret = self.setSpeed(speed)
        return ret
    
    def leftOnDuring(self, duration, speed = SPV_VERYFAST):
        """Move the robot to the left during a number of seconds.
        
        @param duration: duration of the rotation.
        @param speed: speed of the rotation.
        (SPV_VERYSLOW|SPV_SLOW|SPV_NORMAL|SPV_FAST|SPV_VERYFAST)
        @return: the success of the command.
        """
        
        timeout = duration * 2.0
        ret = self.leftOnDuringAsync(duration, speed)
        if self.__parent.server.getClientLevel() == CLIENT_LEVEL_ANONYME:
            return ret
        if ret:
            ret = self.waitLeftMovingOff(timeout)
        return ret
    
    def rightOnDuring(self, duration, speed = SPV_VERYFAST):
        """Move the robot to the right during a number of seconds.
        
        @param duration: duration of the rotation.
        @param speed: speed of the rotation.
        (SPV_VERYSLOW|SPV_SLOW|SPV_NORMAL|SPV_FAST|SPV_VERYFAST)
        @return: the success of the command.
        """
        
        timeout = duration * 2.0
        ret = self.rightOnDuringAsync(duration, speed)
        if self.__parent.server.getClientLevel() == CLIENT_LEVEL_ANONYME:
            return ret
        if ret:
            ret = self.waitRightMovingOff(timeout)
        return ret
    
    def getLeftMovingState(self):
        """Get the left rotation state of the robot.
        
        @return: a boolean.
        """
        value, delay = self.__parent.status.requestOne(ST_NAME_SPIN_LEFT_MOTOR_ON)
        if value in [None, "False"]:
            return False
        else:
            return True
    
    def waitLeftMovingOff(self, timeout):
        """Wait that the robot don't turn to the left.
        Not available for CLIENT_LEVEL_ANONYME level.
        
        @param timeout: maximal delay to wait.
        @return: the state of the wait result.
        """
        if self.__parent.server.getClientLevel() == CLIENT_LEVEL_ANONYME:
            raise TuxAPIExceptionCL, self.__parent.server.getClientLevel()
        return self.__parent.event.handler.waitCondition(ST_NAME_SPIN_LEFT_MOTOR_ON, 
                            ("False", None), timeout)
        
    def getRightMovingState(self):
        """Get the right rotation state of the robot.
        
        @return: a boolean.
        """
        value, delay = self.__parent.status.requestOne(ST_NAME_SPIN_RIGHT_MOTOR_ON)
        if value in [None, "False"]:
            return False
        else:
            return True
    
    def waitRightMovingOff(self, timeout):
        """Wait that the robot don't turn to the right.
        Not available for CLIENT_LEVEL_ANONYME level.
        
        @param timeout: maximal delay to wait.
        @return: the state of the wait result.
        """
        if self.__parent.server.getClientLevel() == CLIENT_LEVEL_ANONYME:
            raise TuxAPIExceptionCL, self.__parent.server.getClientLevel()
        return self.__parent.event.handler.waitCondition(ST_NAME_SPIN_RIGHT_MOTOR_ON, 
                            ("False", None), timeout)
    