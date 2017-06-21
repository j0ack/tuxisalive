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

from TuxHTTPRequest import TuxHTTPRequest
from TuxAPIConst import *
from TuxAPIMisc import checkValue
from TuxAPIExceptionCL import TuxAPIExceptionCL

class TuxAPIServer(object):
    """TuxAPIServer is a module part of TuxAPI. This class make a connection 
    to the Tuxdroid HTTP REST server.
    """
    
    def __init__(self, parent, host = '127.0.0.1', port = 270):
        """Constructor of the class.
        
        @param host: host of the server.
        @param port: port of the server.
        """
        # Parent object (TuxAPI)
        if str(type(parent)).find(".TuxAPI'") != -1:
            self.__parent = parent
            self.__eventHandlers = parent.getEventHandlers()
            self.__connectedEventHandler = self.__eventHandlers.getEventHandler(ST_NAME_API_CONNECT)
        else:
            self.__parent = None
            self.__eventHandlers = None
            self.__connectedEventHandler = None
        # Server field
        self.__host = host
        self.__port = port
        self.__cmdUrl = "0/"
        self.__cmdUrlMutex = threading.Lock()
        # Client field
        self.__clientName = None
        self.__clientPasswd = None
        self.__clientId = 0
        self.__clientLevel = CLIENT_LEVEL_ANONYME
        # Connection field
        self.__connected = False
        self.__connectedLU = time.time()
        self.__connectedMutex = threading.Lock()
        # Auto connection field
        self.__autoConnectionRun = False
        self.__autoConnectionMutex = threading.Lock()
        self.__autoConnectionThread = None
        self.__autoConnectionLoopDelay = 1.0
        # Sender field
        self.__sender = TuxHTTPRequest(host, port)
        
    def destroy(self):
        """destructor of the class.
        """
        self.__autoConnectionStop()
        self.disconnect()
        
    def getClientLevel(self):
        """Get the client level of the API instance.
        
        @return: the client level
        """
        return self.__clientLevel
    
    def __setCmdUrl(self, value):
        """
        """
        self.__cmdUrlMutex.acquire()
        self.__cmdUrl = value
        self.__cmdUrlMutex.release()
        
    def __getCmdUrl(self):
        """
        """
        self.__cmdUrlMutex.acquire()
        value = self.__cmdUrl
        self.__cmdUrlMutex.release()
        return value
    
    def __setConnected(self, value):
        """
        """
        self.__connectedMutex.acquire()
        self.__connected = value
        self.__connectedMutex.release()
        
        if self.__connectedEventHandler != None:
            currentTime = time.time()
            lU = currentTime - self.__connectedLU
            if value:
                self.__connectedEventHandler.emit("True", lU)
            else:
                self.__connectedEventHandler.emit("False", lU)
            self.__connectedLU = currentTime
            
    def __setDisconnected(self):
        if not self.getConnected():
            return
        self.__clientName = None
        self.__clientPasswd = None
        self.__clientLevel = None
        self.__setConnected(False)
        self.__setCmdUrl("0/")
        print "TuxAPI is disconnected."
        
    def getConnected(self):
        """Return the state of connection to the server.
        """
        self.__connectedMutex.acquire()
        value = self.__connected
        self.__connectedMutex.release()
        return value
    
    def waitConnected(self, timeout = 99999999999.):
        """Wait until the client was connected to the server.
        Not available for CLIENT_LEVEL_ANONYME level.
        
        @param timeout: maximal delay to wait.
        @return: the state of the wait result.
        """
        if self.getClientLevel() == CLIENT_LEVEL_ANONYME:
            raise TuxAPIExceptionCL, self.getClientLevel()
        if not checkValue(timeout, "float"):
            return False
        if self.getConnected():
            return True
        if self.__connectedEventHandler != None:
            return self.__connectedEventHandler.waitCondition(("True", None), timeout)
        else:
            return False
        
    def waitDisconnected(self, timeout = 99999999999.):
        """Wait until the client was disconnected from the server.
        Not available for CLIENT_LEVEL_ANONYME level.
        
        @param timeout: maximal delay to wait.
        @return: the state of the wait result.
        """
        if self.getClientLevel() == CLIENT_LEVEL_ANONYME:
            raise TuxAPIExceptionCL, self.getClientLevel()
        if not checkValue(timeout, "float"):
            return False
        if not self.getConnected():
            return True
        if self.__connectedEventHandler != None:
            return self.__connectedEventHandler.waitCondition(("False", None), timeout)
        else:
            return False
        
    def registerEventOnConnected(self, funct, idx = None):
        """Register a callback on the connected event.
        
        @param funct: pointer to the function.
        @param idx: index from a previous register.
        @return: the new index of the callback in the handler.
        """
        nIdx = -1
        if self.__connectedEventHandler != None:
            nIdx = self.__connectedEventHandler.register(funct, ("True", None), idx)
        return nIdx
    
    def unregisterEventOnConnected(self, idx):
        """Unregister a callback from the connected event.
        
        @param idx: index from a previous register.
        """
        if self.__connectedEventHandler != None:
            self.__connectedEventHandler.unregister(idx)
            
    def registerEventOnDisconnected(self, funct, idx = None):
        """Register a callback on the disconnected event.
        
        @param funct: pointer to the function.
        @param idx: index from a previous register.
        @return: the new index of the callback in the handler.
        """
        nIdx = -1
        if self.__connectedEventHandler != None:
            nIdx = self.__connectedEventHandler.register(funct, ("False", None), idx)
        return nIdx
    
    def unregisterEventOnDisconnected(self, idx):
        """Unregister a callback from the disconnected event.
        
        @param idx: index from a previous register.
        """
        if self.__connectedEventHandler != None:
            self.__connectedEventHandler.unregister(idx)
            
    def request(self, cmd, varStruct = {}, varResult = {}, forceExec = False):
        """Send a request to the server.
        
        @param cmd: formated command in an url.
        @param varStruct: structure definition of the requested values.
        @param varResult: returned values in a structure.
        @param forceExec: force the sending of the command when the client is not yet
                         connected.
        @return: the success of the request.
        """
        if not forceExec:
            if not self.getConnected():
                return False
                
        def getValueFromStructure(struct, valuePath):
            pathList = valuePath.split(".")
            node = struct
            result = None
            for i, p in enumerate(pathList):
                # Current node in path is valid
                if node.has_key(p):
                    # Path : leaf
                    if i == len(pathList) - 1:
                        # Return the value of the matched path
                        result = node[p]
                        return result
                    # Path : node
                    else:
                        node = node[p]
                # Invalid path
                else:
                    return result
            return result
            
        # Completing the command
        cmd = "%s%s" % (self.__getCmdUrl(), cmd)
        # Send the request and get the xml structure
        xmlStruct = self.__sender.request(cmd)
        # Check server run and the command success
        if xmlStruct['server_run'] != "Success":
            # Server seems to be disconnected
            self.__setDisconnected()
            return False
        if xmlStruct['result'] != "Success":
            return False
        # Get values from paths
        if len(varStruct.keys()) > 0:
            for valueName in varStruct.keys():
                valuePath = varStruct[valueName]
                value = getValueFromStructure(xmlStruct, valuePath)
                varResult[valueName] = value
        else:
            for key in xmlStruct.keys():
                varResult[key] = xmlStruct[key]
            
        return True
    
    def getVersion(self):
        """Get the HTTP server version.
        
        @return: the version of the HTTP server.
        """
        varStruct = {
            "version" : "data0.version",
        }
        varResult = {}
        if self.request("version?", varStruct, varResult, True):
            return varResult["version"]
        else:
            return ""
            
    def connect(self, level, name, passwd):
        """Attempt to connect to the server.
        
        @param level: requested level of the client.
        @param name: name of the client.
        @param passwd: password of the client.
        @return: the success of the connection.
        """
        # If already connected - Success
        if self.getConnected():
            return True
        # If client level is invalid - Failed
        if level not in CLIENT_LEVELS:
            return False
        self.__clientLevel = level
        # If client level is ANONYME - Success
        if level == CLIENT_LEVEL_ANONYME:
            cmdUrl = "0/"
            self.__setCmdUrl(cmdUrl)
            self.__setConnected(True)
            return True
        # Check name and passw type
        if not checkValue(name, 'str'):
            return False
        if not checkValue(passwd, 'str'):
            return False
        # Make command
        cmd = "client/create?level=%d&name=%s&passwd=%s" % (level, name, passwd)
        varStruct = {
            'client_id' : 'data0.client_id',
        }
        varResult = {}
        # Request
        if not self.request(cmd, varStruct, varResult, forceExec = True):
            return False
        # Check client_id
        if varResult['client_id'] in ['-1', None]:
            return False
        # Ok !!!
        self.__clientName = name
        self.__clientPasswd = passwd
        cmdUrl = "%s/" % varResult['client_id']
        self.__setCmdUrl(cmdUrl)
        self.__setConnected(True)
        print "TuxAPI is connected."
        
        return True
    
    def disconnect(self):
        """Disconnect the client from the server.
        """
        # If already disconnected - Success
        if not self.getConnected():
            return True
        # Make command
        cmd = "client/destroy?passwd=%s" % self.__clientPasswd
        varStruct = {}
        varResult = {}
        # Request
        if not self.request(cmd, varStruct, varResult):
            return False
        # OK !!!
        self.__autoConnectionStop()
        self.__setDisconnected()
        return True
    
    def __setAutoConnectionRun(self, value):
        """
        """
        self.__autoConnectionMutex.acquire()
        self.__autoConnectionRun = value
        self.__autoConnectionMutex.release()
    
    def __getAutoConnectionRun(self):
        """
        """
        self.__autoConnectionMutex.acquire()
        value = self.__autoConnectionRun
        self.__autoConnectionMutex.release()
        return value
    
    def autoConnect(self, level, name, passwd):
        """Start the automatic connection/reconnection loop with the server.
        Not available for CLIENT_LEVEL_ANONYME level.
        
        @param level: requested level of the client.
        @param name: name of the client.
        @param passwd: password of the client.
        """
        if level == CLIENT_LEVEL_ANONYME:
            raise TuxAPIExceptionCL, level
        if self.__getAutoConnectionRun():
            return
        self.__autoConnectionThread = threading.Thread(target = self.__autoConnectionLoop,
            args = (level, name, passwd))
        self.__autoConnectionThread.start()
        self.__clientLevel = level
    
    def __autoConnectionStop(self):
        """
        """
        if not self.__getAutoConnectionRun():
            return
        self.__setAutoConnectionRun(False)
        time.sleep(self.__autoConnectionLoopDelay)
        if self.__autoConnectionThread != None:
            if self.__autoConnectionThread.isAlive():
                self.__autoConnectionThread._Thread__stop()
                
    def __autoConnectionLoop(self, level, name, passwd):
        """
        """
        self.__setAutoConnectionRun(True)
        while self.__getAutoConnectionRun():
            if not self.getConnected():
                self.connect(level, name, passwd)
            # Wait before the next cycle 
            time.sleep(self.__autoConnectionLoopDelay)
            
if __name__ == "__main__":
    print "Create a TuxAPIServer to (127.0.0.1:270)"
    cliServ = TuxAPIServer(None, host = '127.0.0.1', port = 270)
    print "Start the auto connection loop"
    cliServ.autoConnect(CLIENT_LEVEL_FREE, "Test", "myPasswd")
    print "Wait connected ..."
    cliServ.waitConnected(10.0)
    
    if cliServ.getConnected():
        print "Wait disconnected ..."
        cliServ.waitDisconnected(10.0)
    print "Destroy the client ..."
    cliServ.destroy()
    print "... Finish"
        