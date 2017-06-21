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

from TuxAPIMisc import checkValue
from TuxAPIExceptionCL import TuxAPIExceptionCL

class TuxAPIStatus(object):
    """
    """
    
    def __init__(self, parent):
        """Constructor of the class.
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
            
    def requestOne(self, statusName):
        """Get the value and delay of a status.
        """
        if not checkValue(statusName, "str"):
            return None, None
        cmd = "status/request_one?status_name=%s" % statusName
        varStruct = {
            "value" : "data0.value",
            "delay" : "data0.delay",
        }
        varResult = {}
        if self.__parent != None:
            # Request
            if self.__parent.server.request(cmd, varStruct, varResult):
                return varResult["value"], varResult["delay"]
        return None, None
    
    def send(self, statusName, statusValues, encoding = "latin-1"):
        """Send a status.
        
        @param statusName: name of the status.
        @param statusValues: values of the status as list.
        @param encoding: encoding format of the source.
            ( By example, the encoding must be set with sys.stdin.encoding if
              the status is sent from Tuxshell. The encoding must be set to 
              "utf-8" if the status is sent from a python script coded in utf-8)
        @return: the success of the command.
        """
        if not checkValue(statusName, "str"):
            return False
        if not checkValue(statusValues, "list"):
            return False
        if len(statusValues) == 0:
            return False
        for statusValue in statusValues:
            if not checkValue(statusValue, "str"):
                return False
        valuesStr = ""
        for statusValue in statusValues:
            valuesStr += "%s|" % statusValue
        valuesStr = valuesStr[:-1]
        try:
            u = unicode(valuesStr, encoding)
            valuesStr = u.encode("latin-1", 'replace')
        except:
            pass
        try:
            u = statusName.decode(encoding)
            statusName = u.encode("latin-1", 'replace')
        except:
            pass
        pcmd = urllib.urlencode({'name' : statusName, 'value' : valuesStr,})
        cmd = "status/send?%s" % pcmd
        if self.__parent != None:
            # Request
            if self.__parent.server.request(cmd, {}, {}):
                return True
        return False
    
    def wait(self, statusName, condition = None, timeout = 999999999.0):
        """Wait a specific state of a status.
        Not available for CLIENT_LEVEL_ANONYME level.
        
        @param statusName: name of the status.
        @param condition: list of the rules of the condition.
        @param timeout: maximal delay to wait.
        @return: the success of the waiting.
        """
        if self.__parent.server.getClientLevel() == CLIENT_LEVEL_ANONYME:
            raise TuxAPIExceptionCL, self.__parent.server.getClientLevel()
        if not checkValue(statusName, "str"):
            return False
        if not checkValue(timeout, "float"):
            return False
        if condition != None:
            if not checkValue(condition, "tuple"):
                return False
        
        return self.__parent.event.handler.waitCondition(statusName, condition, timeout)