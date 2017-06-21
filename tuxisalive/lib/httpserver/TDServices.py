# -*- coding: latin1 -*-

import version
__author__ = version.author
__date__ = version.date
__version__ = version.version
__licence__ = version.licence
del version

#    Copyright (C) 2008 C2ME Sa
#    R�mi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

import copy

from TDClientController import *
from TDError import *
from tuxisalive.lib.misc import SimpleXMLStruct
import time

DEFAULT_CONTENT_STRUCT = {
    'root' : {
        'result' : getStrError(E_TDREST_ACCESSDENIED),
    },
}

DEFAULT_HEADERS = [
            ['Content-type', 'text/xml; charset="utf-8"'],
]

def parseParameters(parameters, expectedFmt):
    result = {}
    
    for key in expectedFmt.keys():
        if parameters.has_key(key):
            try:
                value = eval(parameters[key])
            except:
                value = parameters[key]
                
            fmt = expectedFmt[key]
            
            if fmt == "uint8":
                if str(type(value)) == "<type 'int'>":
                    if (value >= 0) and (value <= 255):
                        result[key] = value
                    else:
                        return False, {}
                else:
                    return False, {}
                    
            elif fmt == "int8":
                if str(type(value)) == "<type 'int'>":
                    if (value >= -128) and (value <= 127):
                        result[key] = value
                    else:
                        return False, {}
                else:
                    return False, {}
                    
            elif fmt == "int":
                if str(type(value)) == "<type 'int'>":
                    result[key] = value
                else:
                    return False, {}
                    
            elif fmt == "float":
                if str(type(value)) == "<type 'float'>":
                    result[key] = value
                else:
                    return False, {}
                    
            elif fmt == "bool":
                if str(type(value)) == "<type 'bool'>":
                    result[key] = value
                else:
                    return False, {}
            
            elif fmt == "string":
                if str(type(value)) == "<type 'str'>":
                    result[key] = value
                else:
                    return False, {}
                    
            elif fmt.find("<") == 0:
                if str(type(value)) != "<type 'str'>":
                    value = str(value)
                ide = fmt.find(">")
                fmt = fmt[1:ide]
                vals = fmt.split("|")
                if value in vals:
                    result[key] = value
                else:
                    return False, {}
                    
            elif fmt == "all":
                result[key] = str(value)
                    
            else:
                return False, {}
                    
        else:
            return False, {}
            
    return True, result

class TDServiceObject(object):

    def __init__(self, accessLevel, clientController):
        self.__accessLevel = accessLevel
        self.__clientController = clientController
        self.__headerContentFunct = None
        self.__lastClientCheckTime = time.time()
        self.__defaultContentXML = SimpleXMLStruct.structToXML(copy.deepcopy(DEFAULT_CONTENT_STRUCT), 
                                                               True)
        
    def setHeaderContentFunct(self, funct):
        self.__headerContentFunct = funct
        
    def getHeaderContent(self, idClient, parameters):
        headers = DEFAULT_HEADERS
        content = self.__defaultContentXML

        # If the id client is registered
        if (self.__lastClientCheckTime + 1.0) < time.time():
            self.__lastClientCheckTime = time.time()
            self.__clientController.refreshClientsTable()
        if self.__clientController.clientExists(idClient):
            client = self.__clientController.getClient(idClient)
            clientLevel = client.getLevel()
            # If the client have the right to perform this service
            if (clientLevel >= self.__accessLevel):
                # If the client have the access to the ressource or
                # the service have his level to ANONYMOUS
                if client.checkAccess() or (self.__accessLevel == \
                    TDCC_LEVEL_ANONYMOUS):
                    if self.__headerContentFunct != None:
                        headers, content = self.__headerContentFunct(idClient
                                            , parameters)
        # If the id client is not registered
        else:
            # If the service have his level to ANONYMOUS
            if self.__accessLevel == TDCC_LEVEL_ANONYMOUS:
                if self.__headerContentFunct != None:
                    headers, content = self.__headerContentFunct(idClient,
                                            parameters)
            # If the service have his level to FREE_CLIENT or RETRICTED_CLIENT
            # and the id_client is 0 (ANONYMOUS client)
            elif (self.__accessLevel in [TDCC_LEVEL_FREE_CLIENT, \
                   TDCC_LEVEL_RESTRICTED_CLIENT]) and \
                  (idClient == 0):
                if self.__headerContentFunct != None:
                    headers, content = self.__headerContentFunct(idClient,
                                            parameters)
                                            
        return headers, content

class TDServiceContainer(object):

    def __init__(self, httpServer):
        self.__httpServer = httpServer
        self.clientCtrl = TDClientController()
        self.__services = []
        
    def createService(self, sPath, level, funct, ressourceName = None, 
        synopsis = None, pFmt = None):
        
        newService = TDServiceObject(level, self.clientCtrl)
        newService.setHeaderContentFunct(funct)
        s_p = self.__httpServer.registerService(None, sPath, 
                newService.getHeaderContent)
        service = [
            sPath,
            level,
            s_p,
            ressourceName,
            synopsis,
            pFmt,
        ]
        self.__services.append(service)
        
    def servicesToStruct(self):
        struct = {
            'root' : {},
        }
        
        res = []
        res.append('NA')
        for service in self.__services:
            if service[3] != None:
                if service[3] not in res:
                    res.append(service[3])
            else:
                service[3] = "NA"
        res.sort()
        
        j = 0
        for resName in res:
            rName = "resource|%d" % j
            j += 1
            struct['root'][rName] = {}
            struct['root'][rName]['name'] = resName
            i = 0
            for service in self.__services:
                if service[3] != None:
                    if service[3] == resName:
                        nName = "service|%d" % i
                        i += 1
                        level = TDCC_LEVEL_NAMES[service[1] + 1]
                        sSt = {
                            'path' : service[0],
                            'level' : level,
                            'synopsis' : service[4],
                        }
                        if service[5] != None:
                            sSt['parameters'] = service[5]
                        struct['root'][rName][nName] = sSt
                        
        return struct
