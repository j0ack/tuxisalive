# -*- coding: utf-8 -*-

import version
__author__ = version.author
__date__ = version.date
__version__ = version.version
__licence__ = version.licence
del version

#    Copyleft (C) 2008 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

import socket
import threading
import time

try:
    from hashlib import md5
except:
    from md5 import md5

from tuxisalive.lib.logger import *

# Formated PING command
_PING_CMD = "PING\n" + "".join(" " * 123)

# ==============================================================================
# Public class
# ==============================================================================

# ------------------------------------------------------------------------------
# Interprocess Notifier Server Class.
# ------------------------------------------------------------------------------
class IPNServer(object):
    """Interprocess Notifier Server Class.
    """

    # --------------------------------------------------------------------------
    # Constructor.
    # --------------------------------------------------------------------------
    def __init__(self, host = '127.0.0.1', port = 271):
        """Constructor.
        @param host: Host IP to listen.
                     Example : '127.0.0.1' for local loop only.
                     Example : '192.168.0.1' for local network only.
                     Example : '' for internet access.
        @param port: TCP port to listen.
        """
        self.__cliLst = []
        self.__cliMutex = threading.Lock()
        self.__socket = None
        self.__host = host
        self.__port = port
        self.__runLst = False
        self.__runLstThread = None
        self.__runLstMutex = threading.Lock()
        self.__runPing = False
        self.__runPingThread = None
        self.__runPingMutex = threading.Lock()
        self.__onClientAdded = None
        self.__onClientRemoved = None
        self.__logger = SimpleLogger("IPNServer_%s" % str(self.__port))
        self.__logger.setTarget(LOG_TARGET_FILE)
        self.__logger.setLevel(LOG_LEVEL_INFO)
        self.__logger.resetLog()
        self.__logger.logInfo("-----------------------------------------------")
        self.__logger.logInfo("IPN v%s" % __version__)
        self.__logger.logInfo("Author : %s" % __author__)
        self.__logger.logInfo("Licence : %s" % __licence__)
        self.__logger.logInfo("-----------------------------------------------")

    # --------------------------------------------------------------------------
    # Register a callback function to the "On client added" event.
    # --------------------------------------------------------------------------
    def registerOnClientAddedCallBack(self, funct):
        """Register a callback function to the "On client added" event.
        @param funct: Function pointer. The function must accept one parameter.
                      Example :
                      def onClientAdded(idClient):
                          print idClient
        """
        self.__onClientAdded = funct

    # --------------------------------------------------------------------------
    # Register a callback function to the "On client removed" event.
    # --------------------------------------------------------------------------
    def registerOnClientRemovedCallBack(self, funct):
        """Register a callback function to the "On client removed" event.
        @param funct: Function pointer. The function must accept one parameter.
                      Example :
                      def onClientRemoved(idClient):
                          print idClient
        """
        self.__onClientRemoved = funct

    # --------------------------------------------------------------------------
    # Check if a client exists.
    # --------------------------------------------------------------------------
    def clientExists(self, id):
        """Check if a client exists.
        @param id: Id client.
        @return: True or False.
        """
        self.__cliMutex.acquire()
        result = False
        for cli in self.__cliLst:
            if cli['id'] == id:
                result = True
                break
        self.__cliMutex.release()
        return result

    # --------------------------------------------------------------------------
    # Start the server.
    # --------------------------------------------------------------------------
    def start(self):
        """Start the server.
        @return: The success of the server start. True or False.
        """
        # Exit the function if the server is already started
        if self.__getRunLst():
            return True
        # Create the server socket
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # Bind the socket
            self.__socket.bind((self.__host, self.__port))
            # Set the socket to listen mode
            self.__socket.listen(50)
            #Run the listen loop and the ping loop
            self.__runLstThread = threading.Thread(target = self.__listenLoop)
            self.__runLstThread.start()
            self.__runPingThread = threading.Thread(target = self.__pingLoop)
            self.__runPingThread.start()
            time.sleep(0.1)
            # Server successfuly started
            self.__logger.logInfo("Server successfully started (%s:%d)" % (
                self.__host, self.__port))
            return True
        except socket.timeout:
            self.__setRunLst(False)
            # Failed to start the server
            self.__logger.logError("Failed to start the server (%s:%d) : %s" % (
                self.__host, self.__port, "Socket.timeout"))
            return False
        except socket.error:
            self.__setRunLst(False)
            # Failed to start the server
            self.__logger.logError("Failed to start the server (%s:%d) : %s" % (
                self.__host, self.__port, "Socket.error"))
            return False
        except:
            self.__setRunLst(False)
            # Failed to start the server
            self.__logger.logError("Failed to start the server (%s:%d) : %s" % (
                self.__host, self.__port, "Unexpected error"))
            return False

    # --------------------------------------------------------------------------
    # Stop the server.
    # --------------------------------------------------------------------------
    def stop(self):
        """Stop the server.
        """
        # If the server don't runs then exit the function
        if not self.__getRunLst():
            return
        # Stop the listen loop
        self.__setRunLst(False)
        # Stop the ping loop
        self.__setRunPing(False)
        # Close the server socket
        self.__socket.close()
        time.sleep(0.1)
        # Ensure that the threads have been stopped
        if self.__runLstThread.isAlive():
            self.__runLstThread._Thread__stop()
        if self.__runPingThread.isAlive():
            self.__runPingThread.join()
        # Clear the clients list
        self.__clearClients()
        self.__logger.logInfo("Server successfully stopped")

    # --------------------------------------------------------------------------
    # Wait that the server has stopped.
    # --------------------------------------------------------------------------
    def waitStop(self):
        """Wait that the server has stopped.
        """
        while self.__getRunLst():
            time.sleep(0.5)
        time.sleep(0.5)

    # --------------------------------------------------------------------------
    # Get the log file path.
    # --------------------------------------------------------------------------
    def getLogFilePath(self):
        """Get the log file path.
        @return: The log file path.
        """
        return self.__logger.getLogFilePath()

    # --------------------------------------------------------------------------
    # Get the state of the listening loop.
    # --------------------------------------------------------------------------
    def __getRunLst(self):
        """Get the state of the listening loop.
        @return: True or False.
        """
        self.__runLstMutex.acquire()
        result = self.__runLst
        self.__runLstMutex.release()
        return result

    # --------------------------------------------------------------------------
    # Set the state of the listening loop.
    # --------------------------------------------------------------------------
    def __setRunLst(self, value = True):
        """Set the state of the listening loop.
        @param value: New value (True or False)
        """
        self.__runLstMutex.acquire()
        self.__runLst = value
        self.__runLstMutex.release()

    # --------------------------------------------------------------------------
    # Get the state of the ping loop.
    # --------------------------------------------------------------------------
    def __getRunPing(self):
        """Get the state of the ping loop.
        @return: True or False.
        """
        self.__runPingMutex.acquire()
        result = self.__runPing
        self.__runPingMutex.release()
        return result

    # --------------------------------------------------------------------------
    # Set the state of the ping loop.
    # --------------------------------------------------------------------------
    def __setRunPing(self, value = True):
        """Set the state of the ping loop.
        @param value: New value (True or False)
        """
        self.__runPingMutex.acquire()
        self.__runPing = value
        self.__runPingMutex.release()

    # --------------------------------------------------------------------------
    # Add a new client in the clients list.
    # --------------------------------------------------------------------------
    def __addClient(self, connection, address):
        """Add a new client in the clients list.
        @param connection: Client socket.
        @param address: Client address.
        """
        self.__cliMutex.acquire()
        # Create a md5 hash of the socket address in order to make an unique
        # identifier for the client.
        md5H = md5()
        md5H.update(str(address[0]) + str(address[1]))
        id = md5H.hexdigest()
        # Create a dictionary for the client configuration
        cliConf = {
            'connection' : connection,
            'address' : address,
            'id' : id,
        }
        # Add the client to the list
        self.__cliLst.append(cliConf)
        # Create a 128 bytes length string with the id client.
        idToSend = id + "\n" + "".join(" " * (127 - len(id)))
        try:
            # Send the identifer to the client
            connection.send(idToSend)
        except:
            pass
        self.__cliMutex.release()
        # Call the "On client added" event
        if self.__onClientAdded != None:
            self.__onClientAdded(id)
        self.__logger.logInfo("New client added (%s)" % id)

    # --------------------------------------------------------------------------
    # Remove a client from the clients list.
    # --------------------------------------------------------------------------
    def __removeClient(self, address):
        """Remove a client from the clients list.
        @param address: Client address.
        """
        self.__cliMutex.acquire()
        removedId = None
        # Search the client address in the registered clients
        for cli in self.__cliLst:
            if cli['address'] == address:
                cli['connection'].close()
                self.__cliLst.remove(cli)
                removedId = cli['id']
                break
        self.__cliMutex.release()
        # If the client has been removed then call the "On client removed" event
        if removedId != None:
            if self.__onClientRemoved != None:
                self.__onClientRemoved(removedId)
        self.__logger.logInfo("Client removed (%s)" % removedId)

    # --------------------------------------------------------------------------
    # Clear the clients list.
    # --------------------------------------------------------------------------
    def __clearClients(self):
        """Clear the clients list.
        """
        self.__cliMutex.acquire()
        self.__cliLst = []
        self.__cliMutex.release()

    # --------------------------------------------------------------------------
    # Socket listening loop.
    # --------------------------------------------------------------------------
    def __listenLoop(self):
        """Socket listening loop.
        """
        self.__setRunLst(True)
        while self.__getRunLst():
            try:
                # Wait for a new client connection. This function is blocking
                # the loop. The parent loop must be killed.
                connection, address = self.__socket.accept()
                # If the client socket is valid then add it to the clients list
                if (connection != None) and (address != None):
                    self.__addClient(connection, address)
            except:
                pass

    # --------------------------------------------------------------------------
    # Ping loop.
    # --------------------------------------------------------------------------
    def __pingLoop(self):
        """Ping loop.
        """
        self.__setRunPing(True)
        while self.__getRunPing():
            aClientHasRemoved = False
            self.__cliMutex.acquire()
            # Ping all clients
            for cli in self.__cliLst:
                try:
                    # Send the PING command
                    cli['connection'].send(_PING_CMD)
                    # Read the client response
                    data = cli['connection'].recv(128)
                except:
                    self.__cliMutex.release()
                    # If an error occuring during the client ping then remove it
                    # from the clients list
                    self.__logger.logInfo("Client socket error (%s)" % \
                        cli['id'])
                    self.__removeClient(cli['address'])
                    aClientHasRemoved = True
                    self.__cliMutex.acquire()
                    break
                if data != "PONG":
                    self.__cliMutex.release()
                    # If the client response is invalid then remove it from the
                    # clients list
                    self.__logger.logInfo("Client not responding (%s)" % \
                        cli['id'])
                    self.__removeClient(cli['address'])
                    aClientHasRemoved = True
                    self.__cliMutex.acquire()
                    break
            self.__cliMutex.release()
            # Wait 2 seconds beetwen the next ping cycle is no client has been
            # removed
            if not aClientHasRemoved:
                time.sleep(2.)

    # --------------------------------------------------------------------------
    # Send a message to the connected clients.
    # --------------------------------------------------------------------------
    def notify(self, message):
        """Send a message to the connected clients.
        @param message: Message to notify. The maximal size of a message is 127
                        characters.
        """
        # Regularize the message length (0 > correct size < 128)
        if len(message) > 127:
            message = message[:126]
        if len(message) == 0:
            message = "NOTIFY"
        message = message + "\n" + "".join(" " * (127 - len(message)))
        self.__logger.logDebug("Notified : (%s)" % message)
        self.__cliMutex.acquire()
        # Send the message to all registered clients
        for cli in self.__cliLst:
            try:
                cli['connection'].send(message)
            except:
                # No special action if the client connection is broken, it will
                # be removed by the "ping" loop
                pass
        # Can't sent another message while 100 msec
        time.sleep(0.1)
        self.__cliMutex.release()
