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

# ==============================================================================
# Public class
# ==============================================================================

# ------------------------------------------------------------------------------
# Interprocess Notifier Client Class.
# ------------------------------------------------------------------------------
class IPNClient(object):
    """Interprocess Notifier Client Class.
    """

    # --------------------------------------------------------------------------
    # Constructor.
    # --------------------------------------------------------------------------
    def __init__(self, host = '127.0.0.1', port = 271):
        """Constructor.
        @param host: Host address of the server.
        @param port: Host port of the server.
        """
        self.__host = host
        self.__port = port
        self.__socket = None
        self.__run = False
        self.__runThread = None
        self.__runMutex = threading.Lock()
        self.__onNotification = None
        self.__onConnected = None
        self.__onDisconnected = None
        self.__notifyThreadsList = []
        self.__ntlMutex = threading.Lock()
        self.__id = "0"

    # --------------------------------------------------------------------------
    # Get the indentifier of the client.
    # --------------------------------------------------------------------------
    def getId(self):
        """Get the indentifier of the client.
        @return: The identifier if connected ortherwise '0' as string.
        """
        return self.__id

    # --------------------------------------------------------------------------
    # Register a callback function to the "On notification" event.
    # --------------------------------------------------------------------------
    def registerOnNotificationCallBack(self, funct):
        """Register a callback function to the "On notification" event.
        @param funct: Function pointer. The function must accept one parameter.
                      Example :
                      def onNotification(message):
                          print message
        """
        self.__onNotification = funct

    # --------------------------------------------------------------------------
    # Register a callback function to the "On connected" event.
    # --------------------------------------------------------------------------
    def registerOnConnectedCallBack(self, funct):
        """Register a callback function to the "On connected" event.
        @param funct: Function pointer. The function must accept one parameter.
                      Example :
                      def onConnected(identifier):
                          print "Client connected with identifier :", identifier
        """
        self.__onConnected = funct

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def registerOnDisconnectedCallBack(self, funct):
        """Register a callback function to the "On disconnected" event.
        @param funct: Function pointer.
                      Example :
                      def onDisconnected():
                          print "Client disconnected"
        """
        self.__onDisconnected = funct

    # --------------------------------------------------------------------------
    # Start the client.
    # --------------------------------------------------------------------------
    def start(self):
        """Start the client.
        @return: The success of the client start.
        """
        # Exit the function if the client is already started
        if self.__getRun():
            return True
        # Create the client socket
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set the socket to blocking mode before to connect it to the server
        self.__socket.setblocking(1)
        try:
            # Connect the client to the server
            self.__socket.connect((self.__host, self.__port))
            # Read my client identifier
            self.__id = self.__socket.recv(128).split('\n')[0]
        except socket.timeout:
            self.__setRun(False)
            self.__socket.setblocking(0)
            # Failed to connect the client to the server
            return False
        except socket.error:
            self.__setRun(False)
            self.__socket.setblocking(0)
            # Failed to connect the client to the server
            return False
        # Set the socket to unblocking mode
        self.__socket.setblocking(0)
        # Set the socket timeout to 100 msec
        self.__socket.settimeout(0.1)
        # Call the "On connected" event
        if self.__onConnected != None:
            self.__onConnected(self.__id)
        # Start the message listening loop
        self.__runThread = threading.Thread(target = self.__runLoop)
        self.__runThread.start()
        time.sleep(0.1)
        # The client is successfuly connected to the server
        return True

    # --------------------------------------------------------------------------
    # Stop the client.
    # --------------------------------------------------------------------------
    def stop(self):
        """Stop the client.
        """
        # Exit the function is the client is not started
        if not self.__getRun():
            return
        # Stop the message listening loop
        self.__setRun(False)
        # Ensure that the thread of the message listening loop has been closed
        if self.__runThread.isAlive():
            if not self.__runThread.join(5.0):
                self.__runThread._Thread__stop()

    # --------------------------------------------------------------------------
    # Add thread in the threaded messages list.
    # --------------------------------------------------------------------------
    def __addNotifyThread(self, thread):
        """Add thread in the threaded messages list.
        @param thread: Thread to be added.
        """
        self.__ntlMutex.acquire()
        self.__notifyThreadsList.append(thread)
        self.__ntlMutex.release()

    # --------------------------------------------------------------------------
    # Wait that the client has stopped.
    # --------------------------------------------------------------------------
    def waitStop(self):
        """Wait that the client has stopped.
        """
        while self.__getRun():
            time.sleep(0.5)
        time.sleep(0.5)

    # --------------------------------------------------------------------------
    # Clean the closed thread from the threaded messages list.
    # --------------------------------------------------------------------------
    def __cleanNotifyThreadList(self):
        """Clean the closed thread from the threaded messages list in order to
        avoiding a memory leak issue.
        """
        self.__ntlMutex.acquire()
        newLst = []
        for t in self.__notifyThreadsList:
            if t.isAlive():
                newLst.append(t)
        self.__notifyThreadsList = newLst
        self.__ntlMutex.release()

    # --------------------------------------------------------------------------
    # Stop all threads from the threaded messages list.
    # --------------------------------------------------------------------------
    def __stopNotifyThreadList(self):
        """Stop all threads from the threaded messages list.
        """
        self.__ntlMutex.acquire()
        for t in self.__notifyThreadsList:
            if t.isAlive():
                # Wait for a hypothetical self closing of the thread
                if not t.join(0.1):
                    # Otherwise, kill it
                    t._Thread__stop()
        self.__ntlMutex.release()

    # --------------------------------------------------------------------------
    # Get the connection state of the client.
    # --------------------------------------------------------------------------
    def __getRun(self):
        """Get the connection state of the client.
        @return: True or False.
        """
        self.__runMutex.acquire()
        result = self.__run
        self.__runMutex.release()
        return result

    # --------------------------------------------------------------------------
    # Set the connection state of the client.
    # --------------------------------------------------------------------------
    def __setRun(self, value = True):
        """Set the connection state of the client.
        @param value: New value (True or False)
        """
        self.__runMutex.acquire()
        self.__run = value
        self.__runMutex.release()

    # --------------------------------------------------------------------------
    # Loop listening message.
    # --------------------------------------------------------------------------
    def __runLoop(self):
        """Loop listening message.
        """
        self.__setRun(True)
        while self.__getRun():
            # Remove the closed threads from the threads list (garbage cleaning)
            self.__cleanNotifyThreadList()
            try:
                # Wait a message from the server. (timeout at 100msec, defined
                # in the function "start()")
                data = self.__socket.recv(128)
                # Extract the message from the frame
                data = data.split('\n')[0]
                # If the message is valid
                if len(data) != 0:
                    # It's a PING
                    if data == "PING":
                        # Responding to the server
                        self.__socket.send("PONG")
                        time.sleep(0.01)
                        continue
                    # It a notification message
                    else:
                        if self.__onNotification != None:
                            # Call the "On notification" event through a thread
                            # Store the thread in the threads list in order to
                            # stop all threads at the client closure
                            t = threading.Thread(target = self.__onNotification,
                                args = (data,))
                            self.__addNotifyThread(t)
                            t.start()
                        time.sleep(0.01)
                        continue
            except socket.timeout:
                time.sleep(0.01)
                # No message from the server ...
                continue
            except socket.error:
                time.sleep(0.01)
                # Server connection was broken, exit the loop !
                break
            except:
                time.sleep(0.01)
                # Unexpected error, should never happen ...
                continue
        # The client must be disconnected
        try:
            self.__socket.close()
        except:
            pass
        # Call the "On disconnected" event and reset the client identifier
        if self.__id != "0":
            if self.__onDisconnected != None:
                self.__onDisconnected()
            self.__id = "0"
