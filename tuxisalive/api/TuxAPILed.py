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

import time

from TuxAPIConst import *
from TuxAPIMisc import checkValue

class TuxAPILed(object):
    """Class to control the blue leds.
    """
    
    def __init__(self, parent):
        """Constructor of the class.
        @param parent: parent object.
        @type parent: TuxAPI
        """
        self.left = TuxAPILedBase(parent, "left")
        """Left blue led. 
        @see: TuxAPILedBase
        """
        self.right = TuxAPILedBase(parent, "right")
        """Right blue led. 
        @see: TuxAPILedBase
        """
        self.both = TuxAPILedBase(parent, "both")
        """Both blue leds. 
        @see: TuxAPILedBase
        """
        
    def destroy(self):
        """Destructor of the class.
        """
        pass

class TuxAPILedBase(object):
    """Base class to control a led.
    """
    
    def __init__(self, parent, ledName):
        """Constructor of the class.
        """
        # Parent field
        if str(type(parent)).find(".TuxAPI'") != -1:
            self.__parent = parent
            self.__eventHandlers = parent.getEventHandlers()
        else:
            self.__parent = None
            self.__eventHandlers = None
        
        if ledName == "both":
            self.__ledNamex = LED_NAME_BOTH  
        elif ledName == "left":
            self.__ledNamex = LED_NAME_LEFT   
        elif ledName == "right":
            self.__ledNamex = LED_NAME_RIGHT
            
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
    
    def __changeIntensity(self, fxType, intensity):
        """
        """
        if not checkValue(fxType, "int"):
            return False
        if not checkValue(intensity, "float"):
            return False
        
        if fxType == LFX_NONE:
            cmd = "leds/on?intensity=%f&leds=%s" % (intensity, self.__ledNamex)
        else:
            if fxType == LFX_FADE:
                fxStep = 10
            elif fxType == LFX_STEP:
                fxStep = 3
            fxCType = LFXEX_GRADIENT_NBR
            cmd = "leds/set?fx_speed=0.5&fx_step=%d&fx_type=%s&intensity=%f&leds=%s" % (fxStep,
                    fxCType, intensity, self.__ledNamex)
        return self.__cmdSimpleResult(cmd)
    
    def setIntensity(self, intensity):
        """Set the intensity of the led.
        
        @param intensity: intensity of the led (0.0 .. 1.0)
        @return: the success of the command.
        """
        return self.__changeIntensity(LFX_NONE, intensity)
    
    def on(self, fxType = LFX_NONE):
        """Set the led state to ON.
        
        @param fxType: type of the transition effect.
                      (LFX_NONE|LFX_FADE|LFX_STEP)
        @return: the success of the command.
        """
        return self.__changeIntensity(fxType, 1.0)
    
    def off(self, fxType = LFX_NONE):
        """Set the led state to OFF.
        
        @param fxType: type of the transition effect.
                      (LFX_NONE|LFX_FADE|LFX_STEP)
        @return: the success of the command.
        """
        return self.__changeIntensity(fxType, 0.0)
    
    def blinkDuringAsync(self, speed, duration, fxType = LFX_NONE):
        """Make a pulse effect with the led.
        (Asynchronous)
        
        @param speed: speed of the state changing.
        (SPV_VERYSLOW|SPV_SLOW|SPV_NORMAL|SPV_FAST|SPV_VERYFAST)
        @param duration: duration of the effect.
        @param fxType: type of the transition effect.
                      (LFX_NONE|LFX_FADE|LFX_STEP)
        @return: the success of the command.
        """
        if not checkValue(speed, "int"):
            return False
        if not checkValue(duration, "float"):
            return False
        if not checkValue(fxType, "int"):
            return False
        if speed not in SPV_SPEED_VALUES:
            return False
        
        perSec = speed
        count = int(duration * perSec * 2)
        delay = 1.0 / perSec
        
        if fxType == LFX_NONE:
            cmd = "leds/blink?leds=%s&count=%d&delay=%f" % (self.__ledNamex,
                        count, delay)
        else:
            if fxType == LFX_FADE:
                fxStep = 10
            elif fxType == LFX_STEP:
                fxStep = 2
            fxCType = LFXEX_GRADIENT_NBR
            fxSpeed = delay / 3.0
            cmd = "leds/pulse?count=%d&fx_speed=%f&fx_step=%d&fx_type=%s&leds=%s&max_intensity=1.0&min_intensity=0.0&period=%f" % (count,
                        fxSpeed, fxStep, fxCType, self.__ledNamex, delay)
        return self.__cmdSimpleResult(cmd)
    
    def blinkDuring(self, speed, duration, fxType = LFX_NONE):
        """Make a pulse effect with the led.
        
        @param speed: speed of the state changing.
        (SPV_VERYSLOW|SPV_SLOW|SPV_NORMAL|SPV_FAST|SPV_VERYFAST)
        @param duration: duration of the effect.
        @param fxType: type of the transition effect.
                      (LFX_NONE|LFX_FADE|LFX_STEP)
        @return: the success of the command.
        """
        ret = self.blinkDuringAsync(speed, duration, fxType)
        if ret:
            time.sleep(duration)
        return ret
    
    def blinkAsync(self, speed, count, fxType = LFX_NONE):
        """Make a pulse effect with the led.
        (Asynchronous)
        
        @param speed: speed of the state changing.
        (SPV_VERYSLOW|SPV_SLOW|SPV_NORMAL|SPV_FAST|SPV_VERYFAST)
        @param count: number of blinks.
        @param fxType: type of the transition effect.
                      (LFX_NONE|LFX_FADE|LFX_STEP)
        @return: the success of the command.
        """
        if not checkValue(speed, "int"):
            return False
        if not checkValue(count, "int"):
            return False
        if not checkValue(fxType, "int"):
            return False
        if speed not in SPV_SPEED_VALUES:
            return False
        
        count = count * 2
        delay = 1.0 / speed
        
        if fxType == LFX_NONE:
            cmd = "leds/blink?leds=%s&count=%d&delay=%f" % (self.__ledNamex,
                        count, delay)
        else:
            if fxType == LFX_FADE:
                fxStep = 10
            elif fxType == LFX_STEP:
                fxStep = 2
            fxCType = LFXEX_GRADIENT_NBR
            fxSpeed = delay / 3.0
            cmd = "leds/pulse?count=%d&fx_speed=%f&fx_step=%d&fx_type=%s&leds=%s&max_intensity=1.0&min_intensity=0.0&period=%f" % (count,
                        fxSpeed, fxStep, fxCType, self.__ledNamex, delay)
        return self.__cmdSimpleResult(cmd)
    
    def blink(self, speed, count, fxType = LFX_NONE):
        """Make a pulse effect with the led.
        
        @param speed: speed of the state changing.
        (SPV_VERYSLOW|SPV_SLOW|SPV_NORMAL|SPV_FAST|SPV_VERYFAST)
        @param count: number of blinks.
        @param fxType: type of the transition effect.
                      (LFX_NONE|LFX_FADE|LFX_STEP)
        @return: the success of the command.
        """
        ret = self.blinkAsync(speed, count, fxType)
        if ret:
            delay = 1.0 / speed
            duration = delay * count
            time.sleep(duration)
        return ret
    
    def getState(self):
        """Get the state of the led.
        
        @return: (SSV_ON|SSV_OFF|SSV_CHANGING)
        """
        result = SSV_OFF
        
        if self.__ledNamex == LED_NAME_LEFT:
            result, delay = self.__parent.status.requestOne(ST_NAME_LEFT_LED)
        elif self.__ledNamex == LED_NAME_RIGHT:
            result, delay = self.__parent.status.requestOne(ST_NAME_RIGHT_LED)
        else:
            value, delay = self.__parent.status.requestOne(ST_NAME_LEFT_LED)
            value1, delay = self.__parent.status.requestOne(ST_NAME_RIGHT_LED)
            if value == value1:
                result = value
        return result