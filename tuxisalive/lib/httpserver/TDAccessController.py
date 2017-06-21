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

TDAC_ACCESS_RELEASED                = -1
TDAC_ID_RANGE_ANONYMOUS             = range(-1, 0)
TDAC_ID_RANGE_FREE_CLIENT           = range(1, 254)
TDAC_ID_RANGE_RESTRICTED_CLIENT     = range(255, 65534)
TDAC_ID_RANGE_ROOT                  = range(65535, 65536)

ACCESS_PRIORITY_LOW         = 0
ACCESS_PRIORITY_NORMAL      = 1
ACCESS_PRIORITY_HIGH        = 2
ACCESS_PRIORITY_CRITICAL    = 3
ACCESS_PRIORITIES = [
    ACCESS_PRIORITY_LOW,
    ACCESS_PRIORITY_NORMAL,
    ACCESS_PRIORITY_HIGH,
    ACCESS_PRIORITY_CRITICAL,
]

class TDAccessController(object):

    def __init__(self):
        self.__currentAllowedUser = TDAC_ACCESS_RELEASED
        self.__currentPriorityLevel = ACCESS_PRIORITY_LOW
        self.__mutex = threading.Lock()
        self.__locked = False
        
    def getCurrentAllowedUser(self):
        self.__mutex.acquire()
        result = self.__currentAllowedUser
        self.__mutex.release()
        return result
        
    def acquireAccess(self, idUser, priorityLevel):
        # Priority level not found
        if priorityLevel not in ACCESS_PRIORITIES:
            return False
           
        self.__mutex.acquire()
        currentPriorityLevel = self.__currentPriorityLevel
        self.__mutex.release()
        
        # If client is RESTRICTED_CLIENT    
        if idUser in TDAC_ID_RANGE_RESTRICTED_CLIENT:
            # If the resource access is locked by the root then fail
            if self.getLocked():
                return False
            else:
                self.__mutex.acquire()
                # If the access is released or client already have the access
                if (self.__currentAllowedUser == TDAC_ACCESS_RELEASED) or \
                (self.__currentAllowedUser == idUser) or \
                (priorityLevel > currentPriorityLevel):
                    self.__currentAllowedUser = idUser
                    self.__currentPriorityLevel = priorityLevel
                    self.__mutex.release()
                    return True
                else:
                    self.__mutex.release()
                    return False
        else:
            return True
            
    def getLocked(self):
        self.__mutex.acquire()
        result = self.__locked
        self.__mutex.release()
        return result
        
    def setLocked(self, value = True):
        self.__mutex.acquire()
        self.__locked = value
        self.__mutex.release()
        
    def releaseAccess(self, idUser = None):
        self.__mutex.acquire()
        if (self.__currentAllowedUser == idUser) or \
           (idUser == None):
            self.__currentAllowedUser = TDAC_ACCESS_RELEASED
            self.__currentPriorityLevel = ACCESS_PRIORITY_LOW
        self.__mutex.release()
    
    def checkAccess(self, idUser, priorityLevel):
        # Priority level not found
        if priorityLevel not in ACCESS_PRIORITIES:
            return False
        self.__mutex.acquire()
        currentPriorityLevel = self.__currentPriorityLevel
        self.__mutex.release()
        
        # If client is RESTRICTED_CLIENT    
        if idUser in TDAC_ID_RANGE_RESTRICTED_CLIENT:
            # If the resource access is locked by the root then fail
            if self.getLocked():
                return False
            else:
                self.__mutex.acquire()
                # If the access is released or client have the access
                if (self.__currentAllowedUser == TDAC_ACCESS_RELEASED) or \
                (self.__currentAllowedUser == idUser) or \
                (priorityLevel > currentPriorityLevel) :
                    self.__mutex.release()
                    return True
                else:
                    self.__mutex.release()
                    return False
        else:
            return True
