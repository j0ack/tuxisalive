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

import threading
import time

from IPNServer import IPNServer
from IPNClient import IPNClient

# ==============================================================================
# Server functions
# ==============================================================================

# ------------------------------------------------------------------------------
# Callback function on "client added" event.
# ------------------------------------------------------------------------------
def serverOnClientAdded(idClient):
    print "[Server] New client :", idClient

# ------------------------------------------------------------------------------
# Callback function on "client removed" event.
# ------------------------------------------------------------------------------
def serverOnClientRemoved(idClient):
    print "[Server] Removed client :", idClient

# ------------------------------------------------------------------------------
# Function to create a IPN server.
# ------------------------------------------------------------------------------
def serverProcess(timeout = 100.0):
    serv = IPNServer()
    serv.registerOnClientAddedCallBack(serverOnClientAdded)
    serv.registerOnClientRemovedCallBack(serverOnClientRemoved)
    if serv.start():
        for i in range(int(timeout / 0.1)):
            serv.notify("Hello")
            time.sleep(0.001)
        serv.stop()

# ==============================================================================
# Client functions
# ==============================================================================

# ------------------------------------------------------------------------------
# Callback function on "connected" event.
# ------------------------------------------------------------------------------
def clientOnConnected(id):
    print "[Client] Connected with id : ", id

# ------------------------------------------------------------------------------
# Callback function on "disconnected" event.
# ------------------------------------------------------------------------------
def clientOnDisconnected():
    print "[Client] Disconnected"

# ------------------------------------------------------------------------------
# Callback function on "notification" event.
# ------------------------------------------------------------------------------
def clientOnNotification(message):
    print "[Client] Message :", message

# ------------------------------------------------------------------------------
# Create a IPN client.
# ------------------------------------------------------------------------------
def clientProcess(timeout = 10.0):
    cli = IPNClient()
    #cli.registerOnNotificationCallBack(clientOnNotification)
    cli.registerOnConnectedCallBack(clientOnConnected)
    cli.registerOnDisconnectedCallBack(clientOnDisconnected)
    if cli.start():
        time.sleep(timeout)
        cli.stop()
    else:
        print "Client can't be connected"

# ------------------------------------------------------------------------------
# Test the IPN module.
# ------------------------------------------------------------------------------
def test():
    """Test the IPN module.
    """
    # Create a IPN server
    t = threading.Thread(target = serverProcess, args = (15.0,))
    t.start()
    # Create 50 IPN clients
    for i in range(50):
        t = threading.Thread(target = clientProcess, args = (5.0,))
        t.start()
        time.sleep(0.02)
    time.sleep(14.0)

# ------------------------------------------------------------------------------
# Main
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    test()
