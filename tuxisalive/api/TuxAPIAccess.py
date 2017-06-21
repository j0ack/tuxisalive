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
from TuxAPIExceptionCL import TuxAPIExceptionCL

class TuxAPIAccess(object):
    """Class to control the resource access. When you have your level to
    CLIENT_LEVEL_RESTRICTED, you need to acquiring and releasing the resource.
    It mechanism is needed for the synchronization of the resource access by the
    programs which want using Tuxdroid.
    CLIENT_LEVEL_FREE, CLIENT_LEVEL_ROOT and CLIENT_LEVEL_ANONYME don't have
    this restriction.
    When you make a tux gadget, you must to use the CLIENT_LEVEL_RESTRICTED level.
    (Only by convention ;) )
    """
    
    def __init__(self, parent):
        """Constructor of the class.
        @param parent: parent object.
        @type parent: TuxAPI
        """
        # Parent field
        if str(type(parent)).find(".TuxAPI'") != -1:
            self.__parent = parent
        else:
            self.__parent = None
            
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
    
    def acquire(self, priorityLevel = ACCESS_PRIORITY_NORMAL):
        """ To acquiring the resource access.
        Need for CLIENT_LEVEL_RESTRICTED level.
        Don't forget to release the access after !!!
        Not available for CLIENT_LEVEL_ANONYME level.
        
        @param priorityLevel: (ACCESS_PRIORITY_LOW|ACCESS_PRIORITY_NORMAL|
                              ACCESS_PRIORITY_HIGH|ACCESS_PRIORITY_CRITICAL)
        @return: the success of the acquiring.
        """
        if self.__parent.server.getClientLevel() == CLIENT_LEVEL_ANONYME:
            raise TuxAPIExceptionCL, self.__parent.server.getClientLevel()
        cmd = "access/acquire?priority_level=%d" % priorityLevel
        return self.__cmdSimpleResult(cmd)
    
    def waitAcquire(self, timeout, priorityLevel = ACCESS_PRIORITY_NORMAL):
        """Wait that the resource can be acquired.
        Need for CLIENT_LEVEL_RESTRICTED level.
        Don't forget to release the access after !!!
        
        @param timeout: maximal delay to wait.
        @param priorityLevel: (ACCESS_PRIORITY_LOW|ACCESS_PRIORITY_NORMAL|
                              ACCESS_PRIORITY_HIGH|ACCESS_PRIORITY_CRITICAL)
        @return: the success of the acquiring.
        """
        tBegin = time.time()
        while (not self.acquire(priorityLevel)):
            if (time.time() - tBegin) >= timeout:
                return False
            time.sleep(0.25)
        return True
            
    
    def release(self):
        """To releasing the resource access.
        Need for CLIENT_LEVEL_RESTRICTED level.
        Not available for CLIENT_LEVEL_ANONYME level.
        
        @return: the success of the command.
        """
        if self.__parent.server.getClientLevel() == CLIENT_LEVEL_ANONYME:
            raise TuxAPIExceptionCL, self.__parent.server.getClientLevel()
        cmd = "access/release?"
        return self.__cmdSimpleResult(cmd)
    
    def forcingAcquire(self, idClient):
        """To force the acquisition of the resource by a
        specified client.
        Only available for CLIENT_LEVEL_ROOT level.
        
        @param idClient: idx of the client.
        @return: the success of the command.
        """
        if self.__parent.server.getClientLevel() != CLIENT_LEVEL_ROOT:
            raise TuxAPIExceptionCL, self.__parent.server.getClientLevel()
        cmd = "access/forcing_acquire?id_client=%d" % idClient
        return self.__cmdSimpleResult(cmd)
    
    def forcingRelease(self):
        """To force the releasing of the resource.
        Only available for CLIENT_LEVEL_ROOT level.
        
        @return: the success of the command.
        """
        if self.__parent.server.getClientLevel() != CLIENT_LEVEL_ROOT:
            raise TuxAPIExceptionCL, self.__parent.server.getClientLevel()
        cmd = "access/forcing_release?"
        return self.__cmdSimpleResult(cmd)
    
    def lock(self):
        """To lock the resource access. After it, nobody will can
        acquiring the resource.
        Only available for CLIENT_LEVEL_ROOT level.
        
        @return: the success of the command.
        """
        if self.__parent.server.getClientLevel() != CLIENT_LEVEL_ROOT:
            raise TuxAPIExceptionCL, self.__parent.server.getClientLevel()
        cmd = "access/lock?"
        return self.__cmdSimpleResult(cmd)
    
    def unLock(self):
        """To unlock the resource access.
        Only available for CLIENT_LEVEL_ROOT level.
        
        @return: the success of the command.
        """
        if self.__parent.server.getClientLevel() != CLIENT_LEVEL_ROOT:
            raise TuxAPIExceptionCL, self.__parent.server.getClientLevel()
        cmd = "access/unlock?"
        return self.__cmdSimpleResult(cmd)