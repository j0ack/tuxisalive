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
import copy
import time

from TDAccessController import *
from tuxisalive.lib.logger import *

TDCC_LEVEL_ANONYMOUS                = -1
TDCC_LEVEL_FREE_CLIENT              = 0
TDCC_LEVEL_RESTRICTED_CLIENT        = 1
TDCC_LEVEL_ROOT                     = 2

TDCC_LEVEL_NAMES = [
    "ANONYMOUS",
    "FREE_CLIENT",
    "RETRICTED_CLIENT",
    "ROOT",
]

TDCC_INVALID_CLIENT                 = -1

CLIENT_ACTIVITY_TIMEOUT             = 10.0

class TDClientController(object):

    def __init__(self):
        self.__accessController = TDAccessController()
        self.__clients = []
        self.__clientsMutex = threading.Lock()
        self.__logger = SimpleLogger("httpserver")
        self.__logger.setLevel(LOG_LEVEL_INFO)
        self.__logger.setTarget(LOG_TARGET_BOTH)
        
    def destroy(self):
        clients = self.getClientsList()
        for client in clients:
            try:
                client.destroy()
            except:
                pass
            
    def getClientsList(self):
        self.__clientsMutex.acquire()
        clients = copy.copy(self.__clients)
        self.__clientsMutex.release()
        return clients
        
    def setClientsList(self):
        self.__clientsMutex.acquire()
        self.__clients = copy.copy(clients)
        self.__clientsMutex.release()
        
    def clientExists(self, idClient):
        clients = self.getClientsList()
        for client in clients:
            try:
                if client.getId() == idClient:
                    return True
            except:
                pass
        
        return False
        
    def getClient(self, idClient):
        if self.clientExists(idClient):
            clients = self.getClientsList()
            for client in clients:
                try:
                    if client.getId() == idClient:
                        return client
                except:
                    pass
        else:
            return None
            
    def getClients(self):  
        return self.getClientsList()
            
    def __createClient(self, id, level, name, passwd):
        newClient = TDClientObject(id, level, self.__accessController,
                            name, passwd)
        self.__clientsMutex.acquire()
        self.__clients.append(newClient)
        self.__clientsMutex.release()
            
    def createClient(self, clientLevel, name, passwd):
        newId = TDCC_INVALID_CLIENT
        
        # Create a root client       
        if clientLevel == TDCC_LEVEL_ROOT:
            for i in TDAC_ID_RANGE_ROOT:
                if not self.clientExists(i):
                    self.__createClient(i, clientLevel, name, passwd)
                    newId = i
                    break
        
        # Create a free client        
        elif clientLevel == TDCC_LEVEL_FREE_CLIENT:
            for i in TDAC_ID_RANGE_FREE_CLIENT:
                if not self.clientExists(i):
                    self.__createClient(i, clientLevel, name, passwd)
                    newId = i
                    break
        
        # Create a restricted client       
        elif clientLevel == TDCC_LEVEL_RESTRICTED_CLIENT:
            for i in TDAC_ID_RANGE_RESTRICTED_CLIENT:
                if not self.clientExists(i):
                    self.__createClient(i, clientLevel, name, passwd)
                    newId = i
                    break
                
        if newId == TDCC_INVALID_CLIENT:
            self.__logger.logInfo("An attempt to create a client was failed.")
        else:
            self.__logger.logInfo("Create new client : (%s:%s:%d) : %d" % (name, passwd,
                    clientLevel, newId))
        return newId
    
    def destroyClient(self, clientId):
        if self.clientExists(clientId):
            client = self.getClient(clientId)
            try:
                client.destroy()
            except:
                pass
            self.__clientsMutex.acquire()
            self.__clients.remove(client)
            self.__clientsMutex.release()
            self.__logger.logInfo("Client (%d) was destroyed." % clientId)
            
    def refreshClientsTable(self):
        clientsToDestroy = []
        clients = self.getClientsList()
        for client in clients:
            try:
                if not client.checkActivity():
                    clientsToDestroy.append(client)
            except:
                pass
        for client in clientsToDestroy:
            self.destroyClient(client.getId())
            
    def pushUserEvents(self, events = []):
        clients = self.getClientsList()
        for client in clients:
            try:
                client.pushUserEvents(events)
            except:
                pass
            
    def pushMiscEvents(self, events = []):
        clients = self.getClientsList()
        for client in clients:
            try:
                client.pushMiscEvents(events)
            except:
                pass
        self.refreshClientsTable()

class TDClientObject(object):

    def __init__(self, id, level, accessController, name, passwd):
        self.__logger = SimpleLogger("httpserver")
        self.__logger.setLevel(LOG_LEVEL_INFO)
        self.__logger.setTarget(LOG_TARGET_BOTH)
        self.__id = id
        self.__level = level
        self.__name = name
        self.__passwd = passwd
        self.__lastAllowedIdClient = None
        self.__myAccessPriorityLevel = ACCESS_PRIORITY_LOW
        self.__lastActivityT = time.time()
        self.__mutex = threading.Lock()
        self.__userEventsStack = TDClientEventStack()
        self.__miscEventsStack = TDClientEventStack()
        self.__accessController = accessController
        
    def destroy(self):
        self.releaseAccess()
        
    def __setLastActivityT(self):
        self.__mutex.acquire()
        self.__lastActivityT = time.time()
        self.__mutex.release()
        
    def __getLastActivityT(self):
        self.__mutex.acquire()
        result = time.time() - self.__lastActivityT
        self.__mutex.release()
        return result
        
    def checkActivity(self):
        if self.__getLastActivityT() > CLIENT_ACTIVITY_TIMEOUT:
            self.__logger.logInfo("Client (%s) seems to be not active." % self.__name)
            return False
        else:
            return True
            
    def notifyActivity(self):
        self.__setLastActivityT()
        
    def getLevel(self):
        return self.__level
        
    def getId(self):
        return self.__id
        
    def getName(self):
        return self.__name
        
    def getPasswd(self):
        return self.__passwd
        
    def setPasswd(self, oldPasswd, newPasswd):
        if (oldPasswd == self.__passwd):
            self.__passwd = newPasswd
            return True
        return False
        
    def pushUserEvents(self, events = []):
        if len(events) != 0:
            if self.__accessController.checkAccess(self.__id, self.__myAccessPriorityLevel):
                self.__userEventsStack.push(events)
                
    def pushMiscEvents(self, events = []):
        if len(events) != 0:
            self.__miscEventsStack.push(events)
            
    def popEvents(self):
        self.notifyActivity()
        events = []
        events = self.__userEventsStack.pop()
        tmpEvents = self.__miscEventsStack.pop()
        for event in tmpEvents:
            events.append(event)
        return events
        
    def checkAccess(self):
        self.notifyActivity()
        return self.__accessController.checkAccess(self.__id, self.__myAccessPriorityLevel)
        
    def acquireAccess(self, priorityLevel):
        self.notifyActivity()
        self.__myAccessPriorityLevel = priorityLevel
        ret = self.__accessController.acquireAccess(self.__id, self.__myAccessPriorityLevel)
        msg = "Client (%s) attempt to acquire the access :" % self.__name
        msg = msg, ret
        self.__logger.logInfo(msg)
        return ret
        
    def releaseAccess(self):
        self.notifyActivity()
        self.__logger.logInfo("Client (%s) release the access." % self.__name)
        self.__accessController.releaseAccess(self.__id)
        
    def forcingReleaseAccess(self):
        self.__accessController.releaseAccess()
        
    def forcingAcquireAccess(self, idClient):
        self.__accessController.releaseAccess()
        return self.__accessController.acquireAccess(idClient)
        
    def lockAccess(self):
        self.notifyActivity()
        self.__lastAllowedIdClient = \
            self.__accessController.getCurrentAllowedUser()
        self.forcingReleaseAccess()
        self.__logger.logInfo("Root client lock the access.")
        self.__accessController.setLocked(True)
        
    def unlockAccess(self):
        self.notifyActivity()
        if self.__lastAllowedIdClient == None:
            return
        self.__accessController.setLocked(False)
        self.forcingAcquireAccess(self.__lastAllowedIdClient)
        self.__logger.logInfo("Root client unlock the access.")
        self.__lastAllowedIdClient = None
        

class TDClientEventStack(object):

    def __init__(self):
        self.__stack = []
        self.__stackMutex = threading.Lock()
        
    def push(self, events = []):
        if len(events) == 0:
            return
        
        self.__stackMutex.acquire()
        for event in events:
            self.__stack.append(event)
        self.__stackMutex.release()
        
    def pop(self):
        result = []
        
        self.__stackMutex.acquire()
        if len(self.__stack) != 0:
            result = copy.copy(self.__stack)
            self.__stack = []
        self.__stackMutex.release()
        
        return result
