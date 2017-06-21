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
from TuxAPIMisc import checkValue
from TuxAPIExceptionCL import TuxAPIExceptionCL

class TuxAPISoundFlash(object):
    """
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
            # Request
            if self.__parent.server.request(cmd, {}, {}):
                return True
        return False
    
    def playAsync(self, track, volume = 100.0):
        """Play a sound from the internal memory.
        (Asynchronous)
        
        @param track: index of the sound.
        @param volume: volume (0.0 .. 100.0)
        @return: the success of the command.
        """
        if not checkValue(track, "int"):
            return False
        if not checkValue(volume, "float", 0.0, 100.0):
            return False
        cmd = "sound_flash/play?track=%d&volume=%f" % (track, volume)
        return self.__cmdSimpleResult(cmd)
        
    def play(self, track, volume = 100.0):
        """Play a sound from the internal memory.
        
        @param track: index of the sound.
        @param volume: volume (0.0 .. 100.0)
        @return: the success of the command.
        """
        if self.playAsync(track, volume):
            if self.__parent.server.getClientLevel() == CLIENT_LEVEL_ANONYME:
                return True
            trackName = "TRACK_%.3d" % track
            self.__eventHandlers.waitCondition(ST_NAME_AUDIO_FLASH_PLAY, (trackName, None), 0.2)
            value, delay = self.__parent.status.requestOne(ST_NAME_AUDIO_FLASH_PLAY)
            if value == trackName:
                self.__eventHandlers.waitCondition(ST_NAME_AUDIO_FLASH_PLAY, ("STOP", None), 70.0)
            return True
        else:
            return False
        
    def reflash(self, wavList):
        """Reflash the sound flash memory.
        Only available for CLIENT_LEVEL_RESTRICTED and CLIENT_LEVEL_ROOT 
        levels.
        
        @param wavList: wave file path list.
        @return: (SOUND_REFLASH_NO_ERROR|SOUND_REFLASH_ERROR_PARAMETERS|
                  SOUND_REFLASH_ERROR_RF_OFFLINE|SOUND_REFLASH_ERROR_WAV|
                  SOUND_REFLASH_ERROR_USB)
        """
        if self.__parent.server.getClientLevel() not in [CLIENT_LEVEL_RESTRICTED, CLIENT_LEVEL_ROOT]:
             raise TuxAPIExceptionCL, self.__parent.server.getClientLevel()
        if not checkValue(wavList, "list"):
            return SOUND_REFLASH_ERROR_PARAMETERS
        if len(wavList) <= 0:
            return SOUND_REFLASH_ERROR_PARAMETERS
        tracks = ""
        for wav in wavList:
            if not checkValue(wav, "str"):
                return SOUND_REFLASH_ERROR_PARAMETERS
            tracks = "%s%s|" % (tracks, wav)
        tracks = tracks[:-1]
        cmd = "sound_flash/reflash?tracks=%s" % tracks
        if not self.__cmdSimpleResult(cmd):
            return SOUND_REFLASH_ERROR_PARAMETERS
        else:
            if self.__eventHandlers.waitCondition(ST_NAME_SOUND_REFLASH_END, (SSV_NDEF, None), 5.0):
                self.__eventHandlers.waitCondition(ST_NAME_SOUND_REFLASH_END, (None, None), 150.0)
            value, delay = self.__parent.status.requestOne(ST_NAME_SOUND_REFLASH_END)
            return value
            