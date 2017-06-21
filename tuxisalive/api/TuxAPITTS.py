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
from TuxAPIExceptionCL import TuxAPIExceptionCL

class TuxAPITTS(object):
    """Class to use the text to speech engine.
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
        self.__encoding = "latin-1"
        self.__locutor = "Ryan"
        self.__pitch = 100
            
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
    
    def __cmdVoiceList(self):
        """
        """
        result = []
        if self.__parent != None:
            # Request
            varStruct = {}
            varResult = {}
            if self.__parent.server.request("tts/voices?", varStruct, varResult):
                dataCount = varResult["data_count"]
                for i in range(dataCount):
                    dataName = "data%d" % i
                    result.append(varResult[dataName]["locutor"][:-2])
        return result
    
    def isConsole(self):
        """Set the current console encoding.
        (Only if the api run in an interactive python context)
        """
        import sys
        self.__encoding = sys.stdin.encoding
        
    def setEncoding(self, encoding = "latin-1"):
        """Set the source encoding. The speak functions need to encode the
        text to speak to "utf-8" before to sending it to the HTTP server.
        
        @param encoding: source encoding
                         example : "latin-1", "utf-8", "cp1252", ...
        """
        self.__encoding = encoding
        
    def setPitch(self, value):
        """Set the pitch of the locutor.
        
        @param value: pitch (50 .. 200)
        """
        if not checkValue(value, 'int', 50, 200):
            return
        self.__pitch = value
    
    def getPitch(self):
        """Get the pitch of the locutor.
        
        @return: the pitch of the locutor.
        """
        return self.__pitch
    
    def setLocutor(self, value):
        """Set the locutor.
        
        @param value: name of the locutor.
        """
        if not checkValue(value, 'str'):
            return
        self.__locutor = value
    
    def getLocutor(self):
        """Get the locutor.
        
        @return: the name of the locutor.
        """
        return self.__locutor
    
    def speakAsync(self, text, locutor = None, pitch = None):
        """Read a text with the text to speak engine.
        (Asynchronous)
        
        @param text: text to speak.
        @param locutor: name of the locutor.
        @param pitch: pitch (50 .. 200)
        @return: the success of the command.
        """
        # Check the text var type
        if not checkValue(text, 'str'):
            return False
        # Set the locutor
        if locutor != None:
            self.setLocutor(locutor)
        cmd = "tts/locutor?name=%s" % self.__locutor
        ret = self.__cmdSimpleResult(cmd)
        if not ret:
            return False
        # Set the pitch
        if pitch != None:
            self.setPitch(pitch)
        cmd = "tts/pitch?value=%d" % self.__pitch
        ret = self.__cmdSimpleResult(cmd)
        if not ret:
            return False
        # Try to encode the string
        try:
            text = text.decode(self.__encoding)
            text = text.encode("utf-8", 'replace')
        except:
            pass
        # Remove ending lines
        text = text.replace("\n", ".")
        # Perform the speech
        mText = urllib.urlencode({'text' : text, })
        cmd = "tts/speak?%s" % mText
        ret = self.__cmdSimpleResult(cmd)
        if not ret:
            return False
        if self.__parent.server.getClientLevel() == CLIENT_LEVEL_ANONYME:
            return ret
        # Wait the speak status
        ret = self.__eventHandlers.waitCondition(ST_NAME_SPEAK_STATUS, (None, None), 5.0)
        if not ret:
            return False
        # Get the speak status
        value, delay = self.__parent.status.requestOne(ST_NAME_SPEAK_STATUS)
        if value == "NoError":
            return True
        else:
            return False
        
    def speakPush(self, text):
        """Push a text in the TTS stack.
        
        @param text: text to speak.
        @return: the success of the command.
        """
        # Check the text var type
        if not checkValue(text, 'str'):
            return False
        # Try to encode the string
        try:
            text = text.decode(self.__encoding)
            text = text.encode("utf-8", 'replace')
        except:
            pass
        # Remove ending lines
        text = text.replace("\n", ".")
        # Perform the speech
        mText = urllib.urlencode({'text' : text, })
        cmd = "tts/stack_speak?%s" % mText
        
        return self.__cmdSimpleResult(cmd)
    
    def speakFlush(self):
        """Stop the current speech and flush the TTS stack.
        
        @return: the success of the command.
        """
        cmd = "tts/stack_flush?"
        return self.__cmdSimpleResult(cmd)
        
        
    def speak(self, text, locutor = None, pitch = None):
        """Read a text with the text to speak engine.
        
        @param text: text to speak.
        @param locutor: name of the locutor.
        @param pitch: pitch (50 .. 200)
        @return: the success of the command.
        """
        if self.speakAsync(text, locutor, pitch):
            if self.__parent.server.getClientLevel() == CLIENT_LEVEL_ANONYME:
                return True
            self.__eventHandlers.waitCondition(ST_NAME_TTS_SOUND_STATE, ("ON", None), 1.0)
            value, delay = self.__parent.status.requestOne(ST_NAME_TTS_SOUND_STATE)
            if value == "ON":
                self.__eventHandlers.waitCondition(ST_NAME_TTS_SOUND_STATE, ("OFF", None), 9999999.0)
            return True
        else:
            return False
        
    def stop(self):
        """Stop the current speech.
        
        @return: the success of the command.
        """
        cmd = "tts/stop?"
        return self.__cmdSimpleResult(cmd)
        
    def setPause(self, value = True):
        """Set the pause state of the tts engine.
        
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
        cmd = "tts/pause?value=%s" % pause
        return self.__cmdSimpleResult(cmd)
        
    def getVoices(self):
        """Return the current available voice list.
        
        @return: a list of string.
        """
        return self.__cmdVoiceList()
    
    def registerEventOnVoiceList(self, funct, idx = None):
        """Register a callback on the voice list event.
        Not available for CLIENT_LEVEL_ANONYME level.
        
        @param funct: pointer to the function.
        @param idx: index from a previous register.
        @return: the new index of the callback in the handler.
        """
        if self.__parent.server.getClientLevel() == CLIENT_LEVEL_ANONYME:
            raise TuxAPIExceptionCL, self.__parent.server.getClientLevel()
        nIdx = -1
        if self.__eventHandlers != None:
            nIdx = self.__eventHandlers.register(ST_NAME_VOICE_LIST, funct, 
                                                 (None, None), idx)
        return nIdx
    
    def unregisterEventOnVoiceList(self, idx):
        """Unregister a callback from the voice list event.
        Not available for CLIENT_LEVEL_ANONYME level.
        
        @param idx: index from a previous register.
        """
        if self.__parent.server.getClientLevel() == CLIENT_LEVEL_ANONYME:
            raise TuxAPIExceptionCL, self.__parent.server.getClientLevel()
        if self.__eventHandlers != None:
            self.__eventHandlers.unregister(ST_NAME_VOICE_LIST, idx)
            
    def registerEventOnSoundOn(self, funct, idx = None):
        """Register a callback on the sound on event.
        Not available for CLIENT_LEVEL_ANONYME level.
        
        @param funct: pointer to the function.
        @param idx: index from a previous register.
        @return: the new index of the callback in the handler.
        """
        if self.__parent.server.getClientLevel() == CLIENT_LEVEL_ANONYME:
            raise TuxAPIExceptionCL, self.__parent.server.getClientLevel()
        nIdx = -1
        if self.__eventHandlers != None:
            nIdx = self.__eventHandlers.register(ST_NAME_TTS_SOUND_STATE, funct, 
                                                 ("ON", None), idx)
        return nIdx
    
    def unregisterEventOnSoundOn(self, idx):
        """Unregister a callback from the sound on event.
        Not available for CLIENT_LEVEL_ANONYME level.
        
        @param idx: index from a previous register.
        """
        if self.__parent.server.getClientLevel() == CLIENT_LEVEL_ANONYME:
            raise TuxAPIExceptionCL, self.__parent.server.getClientLevel()
        if self.__eventHandlers != None:
            self.__eventHandlers.unregister(ST_NAME_TTS_SOUND_STATE, idx)
            
    def registerEventOnSoundOff(self, funct, idx = None):
        """Register a callback on the sound off event.
        Not available for CLIENT_LEVEL_ANONYME level.
        
        @param funct: pointer to the function.
        @param idx: index from a previous register.
        @return: the new index of the callback in the handler.
        """
        if self.__parent.server.getClientLevel() == CLIENT_LEVEL_ANONYME:
            raise TuxAPIExceptionCL, self.__parent.server.getClientLevel()
        nIdx = -1
        if self.__eventHandlers != None:
            nIdx = self.__eventHandlers.register(ST_NAME_TTS_SOUND_STATE, funct, 
                                                 ("OFF", None), idx)
        return nIdx
    
    def unregisterEventOnSoundOff(self, idx):
        """Unregister a callback from the sound off event.
        Not available for CLIENT_LEVEL_ANONYME level.
        
        @param idx: index from a previous register.
        """
        if self.__parent.server.getClientLevel() == CLIENT_LEVEL_ANONYME:
            raise TuxAPIExceptionCL, self.__parent.server.getClientLevel()
        if self.__eventHandlers != None:
            self.__eventHandlers.unregister(ST_NAME_TTS_SOUND_STATE, idx)