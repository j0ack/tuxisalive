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

import urllib

from TuxAPIConst import *
from TuxAPIMisc import checkValue

class TuxAPIWav(object):
    """Class to play a wave files.
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
    
    def playAsync(self, waveFile, begin = 0.0, end = 0.0):
        """Play a wave file.
        (Asynchronous)
        
        @param waveFile: wave file to play.
        @param begin: start seconds.
        @param end: stop seconds.
        @return: the success of the command.
        """
        if not checkValue(waveFile, 'str'):
            return False
        if not checkValue(begin, 'float'):
            return False
        if not checkValue(end, 'float'):
            return False
        params = urllib.urlencode(
            {
                'path' : waveFile, 
                'begin' : begin, 
                'end' : end
            }
        )
        cmd = "wav/play?%s" % params
        return self.__cmdSimpleResult(cmd)
    
    def play(self, waveFile, begin = 0.0, end = 0.0):
        """Play a wave file.
        
        @param waveFile: wave file to play.
        @param begin: start seconds.
        @param end: stop seconds.
        @return: the success of the command.
        """
        if not self.playAsync(waveFile, begin, end):
            return False
        
        if self.__parent.server.getClientLevel() == CLIENT_LEVEL_ANONYME:
            return True
        
        ret = self.__eventHandlers.waitCondition(ST_NAME_WAV_CHANNEL_START, 
                                                 (None, None), 1.0)
        if not ret:
            return False
        value, delay = self.__parent.status.requestOne(ST_NAME_WAV_CHANNEL_START)
        try:
            channel = eval(value)
        except:
            return False
        endStName = WAV_CHANNELS_NAME_LIST[channel]
        value, delay = self.__parent.status.requestOne(endStName)
        if value == "OFF":
            self.__eventHandlers.waitCondition(endStName, ("ON", None), 1.0)
        return self.__eventHandlers.waitCondition(endStName, ("OFF", None), 
                                                  999999.0)
        
    def stop(self):
        """Stop the current wave file.
        
        @return: the success of the command.
        """
        cmd = "wav/stop?"
        return self.__cmdSimpleResult(cmd)
        
    def setPause(self, value = True):
        """Set the pause state of the wave player.
        
        @param value: True or False.
        @return: the success of the command.
        """
        # Check the value var type
        if not checkValue(value, 'bool'):
            return False
        if value:
            pause = "True"
        else:
            pause = "False"
        cmd = "wav/pause?value=%s" % pause
        return self.__cmdSimpleResult(cmd)