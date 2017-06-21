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

from TuxEventHandlers import TuxEventHandlers
from TuxAPIConst import *
from TuxAPIMisc import checkValue
from TuxAPIServer import TuxAPIServer
from TuxAPIEvent import TuxAPIEvent
from TuxAPIAccess import TuxAPIAccess
from TuxAPIMouthEyes import TuxAPIMouthEyes
from TuxAPIFlippers import TuxAPIFlippers
from TuxAPISpinning import TuxAPISpinning
from TuxAPIStatus import TuxAPIStatus
from TuxAPIDongleRadio import TuxAPIDongleRadio
from TuxAPIAttitune import TuxAPIAttitune
from TuxAPILed import TuxAPILed
from TuxAPITTS import TuxAPITTS
from TuxAPISoundFlash import TuxAPISoundFlash
from TuxAPIButton import TuxAPIButton
from TuxAPIWav import TuxAPIWav
from TuxAPIRawCommand import TuxAPIRawCommand

class TuxAPI(object):
    """Main module class to control Tuxdroid.
    """
    
    def __init__(self, host = '127.0.0.1', port = 270):
        """Constructor of the class.
        @param host: host of the server.
        @param port: port of the server.
        """
        self.__eventHandlers = TuxEventHandlers()
        self.__fillEventHandlers()
        self.server = TuxAPIServer(self, host, port)
        """Server object.
        @type: TuxAPIServer
        """
        self.server.registerEventOnConnected(self.__onServerConnected)
        self.server.registerEventOnDisconnected(self.__onServerDisconnected)
        self.event = TuxAPIEvent(self)
        """Event object.
        @type: TuxAPIEvent
        """
        # Access controller
        self.access = TuxAPIAccess(self)
        """Access object.
        @type: TuxAPIAccess
        """
        # Status part
        self.status = TuxAPIStatus(self)
        """Status object
        @type: TuxAPIStatus
        """
        # Mouth part
        self.mouth = TuxAPIMouthEyes(self, ST_NAME_MOUTH_POSITION, ST_NAME_MOUTH_RM,
                                     "mouth")
        """Mouth object
        @type: TuxAPIMouthEyes
        """
        # Eyes part
        self.eyes = TuxAPIMouthEyes(self, ST_NAME_EYES_POSITION, ST_NAME_EYES_RM,
                                     "eyes")
        """Eyes object
        @type: TuxAPIMouthEyes
        """
        # Flippers part
        self.flippers = TuxAPIFlippers(self)
        """Flippers object
        @type: TuxAPIFlippers
        """
        # Spinning part
        self.spinning = TuxAPISpinning(self)
        """Spinning object
        @type: TuxAPISpinning
        """
        # Dongle part
        self.dongle = TuxAPIDongleRadio(self, ST_NAME_DONGLE_PLUG);
        """Dongle object
        @type: TuxAPIDongleRadio
        """
        # Radio part
        self.radio = TuxAPIDongleRadio(self, ST_NAME_RADIO_STATE);
        """Radio object
        @type: TuxAPIDongleRadio
        """
        # Attitune part
        self.attitune = TuxAPIAttitune(self)
        """Attitune object
        @type: TuxAPIAttitune
        """
        # Leds part
        self.led = TuxAPILed(self)
        """Led object
        @type: TuxAPILed
        """
        # TTS part
        self.tts = TuxAPITTS(self)
        """TTS object
        @type: TuxAPITTS
        """
        # Sound flash part
        self.soundFlash = TuxAPISoundFlash(self)
        """Sound flash object
        @type: TuxAPISoundFlash
        """
        # Button part
        self.button = TuxAPIButton(self)
        """Button object
        @type: TuxAPIButton
        """
        # Wav part
        self.wav = TuxAPIWav(self)
        """Wav object
        @type: TuxAPIWav
        """
        # Raw commands part
        self.raw = TuxAPIRawCommand(self)
        """Raw command object
        @type: TuxAPIRawCommand
        """
    
    def destroy(self):
        """Destructor of the class.
        """
        self.raw.destroy()
        self.wav.destroy()
        self.button.destroy()
        self.soundFlash.destroy()
        self.tts.destroy()
        self.led.destroy()
        self.attitune.destroy()
        self.radio.destroy()
        self.dongle.destroy()
        self.spinning.destroy()
        self.flippers.destroy()
        self.eyes.destroy()
        self.mouth.destroy()
        self.status.destroy()
        self.access.destroy()
        self.event.destroy()
        self.server.destroy()
        self.__eventHandlers.destroy()
        
    def getVersion(self):
        """Get the version string of the api.
        
        @return: the version string.
        """
        import version
        verString = "%s-%s" % (version.name, version.version)
        del version
        
        return verString
    
    def getVersions(self):
        """Get the version string of all components from Tuxware.
        
        @return: a dictionary of string:string.
        """
        verDict = {}
        verDict["api"] = self.getVersion()
        v, d = self.status.requestOne(ST_NAME_DRIVER_SYMB_VER)
        verDict["tuxhttpserver"] = self.server.getVersion()
        verDict["libtuxdriver"] = v
        v, d = self.status.requestOne(ST_NAME_OSL_SYMB_VER)
        verDict["libtuxosl"] = v
        v, d = self.status.requestOne(ST_NAME_TUXCORE_SYMB_VER)
        verDict["tuxcore"] = v
        v, d = self.status.requestOne(ST_NAME_TUXAUDIO_SYMB_VER)
        verDict["tuxaudio"] = v
        v, d = self.status.requestOne(ST_NAME_FUXUSB_SYMB_VER)
        verDict["fuxusb"] = v
        v, d = self.status.requestOne(ST_NAME_FUXRF_SYMB_VER)
        verDict["fuxrf"] = v
        v, d = self.status.requestOne(ST_NAME_TUXRF_SYMB_VER)
        verDict["tuxrf"] = v

        return verDict
        
    def __fillEventHandlers(self):
        """
        """
        for statusName in SW_NAME_DRIVER:
            self.__eventHandlers.insert(statusName)
        for statusName in SW_NAME_OSL:
            self.__eventHandlers.insert(statusName)
        for statusName in SW_NAME_API:
            self.__eventHandlers.insert(statusName)
        for statusName in SW_NAME_EXTERNAL:
            self.__eventHandlers.insert(statusName)
        
    def getEventHandlers(self):
        """Get the event handlers of the API.
        """
        return self.__eventHandlers
    
    def __onServerConnected(self, value, delay):
        """
        """
        self.event.start()
        
    def __onServerDisconnected(self, value, delay):
        """
        """
        self.event.stop()

    
if __name__ == "__main__":
    import time
    
    def onAllEvent(name, value, delay):
        print "onAllEvent : ", name, value, delay
        pass
    
    print "Create a TuxAPI object"
    tux = TuxAPI(host = '127.0.0.1', port = 270)
    print "Register the 'all' events callback"
    tux.event.handler.register("all", onAllEvent)
    print "Connect to a Tuxdroid server"
    tux.server.autoConnect(CLIENT_LEVEL_RESTRICTED, "Test", "myPasswd")
    print "Wait server connected (10 seconds )..."
    tux.server.waitConnected(10.0)
    if tux.server.getConnected():
        print "Wait dongle connected (10 seconds )..."
        tux.dongle.waitConnected(10.0)
        print "Dongle connected :", tux.dongle.getConnected()
        if tux.dongle.getConnected():
            print "Wait radio connected (10 seconds )..."
            tux.radio.waitConnected(10.0)
            print "Radio connected :", tux.radio.getConnected()
            if tux.radio.getConnected():
                print "Acquire the resource access :", tux.access.acquire()
                print "Load an attitune."
                tux.attitune.load("http://www.tuxisalive.com/Members/remi/hammer.att")
                print "Play the attitune"
                tux.attitune.play()
                print "Wait 10 seconds"
                time.sleep(10.0)
                print "Stop the attitune."
                tux.attitune.stop()
                print "Open the mouth."
                tux.mouth.open()
                time.sleep(1.0)
                print "Close the mouth."
                tux.mouth.close()
                time.sleep(1.0)
                print "7 movements of mouth."
                tux.mouth.on(7, SSV_CLOSE)
                time.sleep(1.0)
                print "4 seconds of movement of mouth."
                tux.mouth.onDuring(4., SSV_CLOSE)
                print "Close the eyes."
                tux.eyes.close()
                time.sleep(1.0)
                print "Open the eyes."
                tux.eyes.open()
                time.sleep(1.0)
                print "7 movements of eyes."
                tux.eyes.on(7, SSV_OPEN)
                time.sleep(1.0)
                print "4 seconds of movement of eyes."
                tux.eyes.onDuring(4., SSV_OPEN)
                print "Set the flippers to up."
                tux.flippers.up()
                time.sleep(1.0)
                print "Set the flippers to down."
                tux.flippers.down()
                time.sleep(1.0)
                print "7 movements of flippers."
                tux.flippers.on(7, SSV_DOWN, SPV_VERYSLOW)
                time.sleep(1.0)
                print "4 seconds of movement of flippers."
                tux.flippers.onDuring(4., SSV_DOWN)
                print "Turn to to left."
                tux.spinning.leftOn(1.0)
                print "Release the resource access :", tux.access.release()

    print "Destroy the TuxAPI ..."
    tux.destroy()
    print "... Finish"