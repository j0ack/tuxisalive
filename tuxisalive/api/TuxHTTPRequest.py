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
import xml.dom.minidom
from xml.dom.minidom import Node
import httplib
import time

class TuxHTTPRequest(object):
    """TuxHTTPRequest is a sender of request to a Tuxdroid service server.
    The resulting xml data is automatically parsed and returned to a
    data structure.
    """
    
    def __init__(self, host = '127.0.0.1', port = 270):
        """Constructor of the class.
        
        @param host: host of the server.
        @param port: port of the server.
        """
        self.__hostPort = "%s:%d" % (host, port)
        self.__mutex = threading.Lock()
        
    def request(self, cmd, method = "GET"):
        """Make a request to the server.

        @param cmd: formated command in an url.
        @param method: method of the request.
        @return: a data structure.
        """
        cmd = "/%s" % cmd
        xmlStruct = {
            'result' : 'Failed',
            'data_count' : 0,
            'server_run' : 'Failed',
        }
        # Try to connect to the server
        self.__mutex.acquire()
        h = httplib.HTTP(self.__hostPort)
        try:
            h.connect()
        except:
            self.__mutex.release()
            return xmlStruct
        # Create the request
        h.putrequest(method, cmd)
        h.putheader("Accept", "text/html")
        h.putheader("Accept", "text/xml")
        h.putheader("Accept-Charset", "iso-8859-1,*,utf-8")
        h.endheaders()
        # Send the request (try 5 times)
        s = False
        c = 0
        contentLength = 0
        while True:
            try:
                errcode, errmsg, headers = h.getreply()
                contentLength = int(headers['Content-Length'])
                s = True
                break
            except:
                pass
            c += 1
            if c > 5:
                break
            time.sleep(0.05)
            
        if not s:
            self.__mutex.release()
            return xmlStruct
            
        if contentLength > 0:
            # Get the result stream
            f = h.getfile()
            try:
                resultStr = f.read()
                f.close()
            except:
                self.__mutex.release()
                return xmlStruct
            # Attempt to encoding the xml stream to utf-8
            try:
                u = resultStr.decode("latin-1")
                resultStr = u.encode("utf-8")
            except:
                pass
            # Parse the xml
            xmlStruct = self.__parseXml(resultStr)
        else:
            xmlStruct['server_run'] = 'Success'
        
        try:
            h.disconnect()
        except:
            pass
        self.__mutex.release()
        
        return xmlStruct
    
    def __parseXml(self, string):
        """Parse the xml string to a data structure.
        """
        struct = {
            'result' : 'Failed',
            'data_count' : 0,
            'server_run' : 'Success',
        }
        dataCount = 0
        dataNodeName = ""
        
        try:
            root = xml.dom.minidom.parseString(string).firstChild
            for iNode in range(len(root.childNodes)):
                node = root.childNodes.item(iNode)
                if node.firstChild.nodeValue != None:
                    struct[node.nodeName] = node.firstChild.data.encode("utf-8")
                else:
                    subStruct = {}
                    for jNode in range(len(node.childNodes)):
                        node1 = node.childNodes.item(jNode)
                        subStruct[node1.nodeName] = node1.firstChild.data.encode("utf-8")
                    if node.nodeName == "data":
                        dataNodeName = "data%d" % dataCount
                        dataCount += 1
                    else:
                        dataNodeName = node.nodeName
                    struct[dataNodeName] = subStruct
                    
            struct["data_count"] = dataCount
        except:
            pass
            
        return struct
    
if __name__ == "__main__":
    import time
    
    print "You need to start Tuxdroid HTTP REST server to control this class."
    print "Create a HTTPRequest object configured to (127.0.0.1:270)"
    HTTPRequest = TuxHTTPRequest('127.0.0.1', 270)
    time.sleep(1.0)
    print "Make a request to the server ('0/client/listing?') : Command exists and the access is allowed."
    print HTTPRequest.request('0/client/listing?')
    time.sleep(1.0)
    print "Make a request to the server ('client/listing?') : Command exists but the access is denied."
    print HTTPRequest.request('client/listing?')
    time.sleep(1.0)
    print "Make a request to the server ('client/listing1?') : Command doesn't exists."
    print HTTPRequest.request('client/listing1?')
    time.sleep(1.0)
    print "Create a HTTPRequest object configured to an invalid server."
    HTTPRequest = TuxHTTPRequest('localhost1', 270)
    time.sleep(1.0)
    print "Make a request to the server ('client/listing?')"
    print HTTPRequest.request('client/listing?')
    time.sleep(1.0)
    print "... Finish !!!"