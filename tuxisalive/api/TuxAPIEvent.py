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

import threading
import time

from TuxAPIConst import *

class TuxAPIEvent(object):
    """TuxAPIEvent is a module part of TuxAPI. It run an asynchronous loop to retrieve the
    events from Tuxdroid, every 100 msec.
    """
    
    def __init__(self, parent):
        """Constructor of the class.
        @param parent: parent object.
        @type parent: TuxAPI
        """
        # Parent object (TuxAPI)
        if str(type(parent)).find(".TuxAPI'") != -1:
            self.__parent = parent
            self.__eventHandlers = parent.getEventHandlers()
        else:
            self.__parent = None
            self.__eventHandlers = None
        self.handler = self.__eventHandlers
        # Event loop field
        self.__eventLoopThread = None
        self.__eventLoopMutex = threading.Lock()
        self.__eventLoopRun = False
        self.__eventLoopDelay = 0.1
        
    def destroy(self):
        """Destructor of the class.
        """
        self.stop()
        
    def setDelay(self, value):
        """Set the delay of the event loop.
        @param value: Delay in seconds. (default value is 0.1 sec)
        """
        if value < 0.1:
            value = 0.1
        elif value > 2.0:
            value = 2.0
        self.__eventLoopDelay = value
    
    def __getEventLoopRun(self):
        """
        """
        self.__eventLoopMutex.acquire()
        value = self.__eventLoopRun
        self.__eventLoopMutex.release()
        return value
        
    def __setEventLoopRun(self, value):
        """
        """
        self.__eventLoopMutex.acquire()
        self.__eventLoopRun = value
        self.__eventLoopMutex.release()
        
    def start(self):
        """Start the loop of event retrieving.
        """
        if self.__parent.server.getClientLevel() == CLIENT_LEVEL_ANONYME:
            return
        if self.__getEventLoopRun():
            return
        self.__eventLoopThread = threading.Thread(target = self.__eventLoop)
        self.__eventLoopThread.start()
        
    def stop(self):
        """Stop the loop of event retrieving.
        """
        if not self.__getEventLoopRun():
            return
        self.__setEventLoopRun(False)
        time.sleep(self.__eventLoopDelay)
        if self.__eventLoopThread != None:
            if self.__eventLoopThread.isAlive():
                self.__eventLoopThread._Thread__stop()
                
    def __eventLoop(self):
        """
        """
        self.__setEventLoopRun(True)
        while self.__getEventLoopRun():
            # Make command
            cmd = "status/events?"
            varStruct = {}
            varResult = {}
            if self.__eventHandlers != None:
                if self.__parent != None:
                    # Request
                    if self.__parent.server.request(cmd, varStruct, varResult):
                        dataCount = varResult['data_count']
                        for i in range(dataCount):
                            dataName = "data%d" % i
                            try:
                                eventStruct = varResult[dataName]
                                stName = eventStruct["name"]
                                stValue = eventStruct["value"]
                                stDelay = eval(eventStruct["delay"])
                            except:
                                continue
                            # If the status is external, parse-it
                            if stName == SW_NAME_EXTERNAL_STATUS:
                                pList = stValue.split("|")
                                if len(pList) > 0:
                                    self.__eventHandlers.getEventHandler("all").emit(*pList)
                            else:
                                self.__eventHandlers.emit(stName, (stValue, stDelay))
            # Wait before the next cycle        
            time.sleep(self.__eventLoopDelay)