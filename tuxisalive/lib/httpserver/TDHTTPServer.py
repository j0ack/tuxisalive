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

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
import threading
import re
import urllib
import sys
import traceback
import os

from tuxisalive.lib.logger import *

tdServices = []
myMutex = threading.Lock()

class TDHTTPServer(object):
    """
    HTTP Server class
    """

    def __init__(self, port = 80):
        self.__logger = SimpleLogger("tuxhttpserver")
        self.__logger.setLevel(LOG_LEVEL_DEBUG)
        self.__logger.setTarget(LOG_TARGET_BOTH)
        self.__port = port
        self.__started = False
        self.__startedMutex = threading.Lock()
        self.__server = None
        self.__createServer()
            
    def __createServer(self):
        if self.__server != None:
            return False
            
        try:
            if os.name == 'nt':
                self.__server = ThreadedHTTPServer(('127.0.0.1', self.__port),
                    TDHttpRequestHandler)
            else:
                self.__server = ThreadedHTTPServer(('', self.__port),
                    TDHttpRequestHandler)
            self.__logger.logInfo("Create a server on port %d" % self.__port)
        except:
            self.__server = None
            return False
            
        return True
        
    def start(self):
        if self.__getStarted():
            return False
            
        if self.__server == None:
            return False
        
        try:
            self.__setStarted(True) 
            self.__logger.logInfo("Server started.")
            self.__server.serve_forever()  
        except:
            pass
        
        self.__logger.logInfo("Server stopped.")
        self.__setStarted(False) 
        return True
        
    def registerService(self, baseService, name, serviceCallback):
        service = {
            'name' : name,
            'service_callback' : serviceCallback,
            'sub_services' : [],
            'mutex' : threading.Lock(),
        }
        
        if baseService == None:
            services = tdServices
        else:
            services = baseService['sub_services']
        
        services.append(service)
        
        self.__logger.logDebug("Service (%s) has been registered" % name)
        return service
        
    def __setStarted(self, value = True):
        self.__startedMutex.acquire()
        self.__started = value
        self.__startedMutex.release()
        
    def __getStarted(self):
        value = False
        
        self.__startedMutex.acquire()
        value = self.__started
        self.__startedMutex.release()
        
        return value 
    
    def getStarted(self):
        return self.__getStarted() 

    
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

class TDHttpRequestHandler(BaseHTTPRequestHandler):

    def __matchService(self, services, path):
    
        def getService(service, path):
            if path.find(service['name']) == 0:
                path = path[len(service['name']):]
                localSub = None
                if len(service['sub_services']) > 0:
                    for sService in service['sub_services']:
                        tmpSub, path = getService(sService, path)
                        if tmpSub != None:
                            localSub = tmpSub
                            break
                if localSub != None:
                    return localSub, path
                else:
                    return service, path
            else:
                return None, path
        
        id = None
        p = re.compile('/(\d+)/')
        res = p.findall(path)
        if len(res) > 0:
            tmp_id = res[0]
            idx = path.find(tmp_id)
            if idx == 1:
                path = path[idx+len(tmp_id):]
                id = eval(tmp_id)
                
        if len(services) > 0:
            for service in services:
                ss, pp = getService(service, path)
                if ss != None:
                    return ss, pp, id
        else:
            return None, path, id
        
    def __parseParameters(self, paramStr):
        params = {}
        while paramStr.find('&') != -1:
            sep_pos = paramStr.find('&')
            equ_pos = paramStr.find('=')
            if paramStr.find('=') != -1:
                name = paramStr[:equ_pos]
                value = paramStr[equ_pos + 1:sep_pos]
                if (name != '') and (value != ''):
                    params[name] = urllib.unquote_plus(value)
            paramStr = paramStr[sep_pos + 1:]
        if len(paramStr) > 0:
            equ_pos = paramStr.find('=')
            if paramStr.find('=') != -1:
                name = paramStr[:equ_pos]
                value = paramStr[equ_pos + 1:]
                if (name != '') and (value != ''):
                    params[name] = urllib.unquote_plus(value)
        return params
            
    def __getHeaderAndContent(self):
        global myMutex
        
        def formatException():
            fList = traceback.format_exception(sys.exc_info()[0], 
                        sys.exc_info()[1], 
                        sys.exc_info()[2])
            result = ""
            for line in fList:
                result += line
            return result
        
        try:
            self.path = urllib.unquote_plus(self.path)
            #print self.path
            service, paramStr, id = self.__matchService(tdServices, self.path)
            paramDict = self.__parseParameters(paramStr)
            if id == None:
                id = -1 
            if service != None:
                if service['service_callback']:
                    #myMutex.acquire()
                    service['mutex'].acquire()
                    try:
                        ret = service['service_callback'](id, paramDict)
                    except:
                        #myMutex.release()
                        service['mutex'].release()
                        self.__logger = SimpleLogger("tuxhttpserver_resources")
                        self.__logger.setLevel(LOG_LEVEL_DEBUG)
                        self.__logger.setTarget(LOG_TARGET_BOTH)
                        self.__logger.logError("Bugged service : (%s)" % self.path)
                        self.__logger.logError(formatException())
                        return None, None
                    #myMutex.release()
                    service['mutex'].release()
                    return ret
            else:
                self.__logger = SimpleLogger("tuxhttpserver")
                self.__logger.setLevel(LOG_LEVEL_DEBUG)
                self.__logger.setTarget(LOG_TARGET_BOTH)
                self.__logger.logWarning("Server received a wrong request : (%s)" % self.path)
                return None, None
        except:
            self.__logger = SimpleLogger("tuxhttpserver_resources")
            self.__logger.setLevel(LOG_LEVEL_DEBUG)
            self.__logger.setTarget(LOG_TARGET_BOTH)
            self.__logger.logError("Bugged service : (%s)" % self.path)
            self.__logger.logError(formatException())
            return None, None
            
    def __sendHeaders(self, headers, content):
        try:
            if headers != None:
                for header in headers:
                    self.send_header(header[0], header[1])
                if content != None:
                    self.send_header('Content-Length', str(len(content)))
                self.end_headers()
                return True
        except:
            print "Error on sending headers"
            return False
            
    def do_HEADER(self):
        headers, content = self.__getHeaderAndContent()
        
        if (headers == None) and (content == None):
            try:
                self.send_error(404, 'Service Not Found')
            except:
                print "Handle error"
            return
        
        try:        
            self.send_response(200)
            self.__sendHeaders(headers, content)
        except:
            print "Handle error"
        

    def do_GET(self):  
        headers, content = self.__getHeaderAndContent()
        
        if (headers == None) and (content == None):
            try:
                self.send_error(404, 'Service Not Found')
            except:
                print "Handle error"
            return
        
        try:        
            self.send_response(200)
            if not self.__sendHeaders(headers, content):
                return
            if content != None:
                self.wfile.write(content)
                self.wfile.flush()  
        except:
            print "Handle error"
            
    def handle_one_request(self):
        try:
            BaseHTTPRequestHandler.handle_one_request(self)
        except:
            print "handle_one_request error"
            
    def log_request(self, code='-', size='-'):
        pass
    