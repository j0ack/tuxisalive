# -*- coding: utf-8 -*-

import version
__author__ = version.author
__date__ = version.date
__version__ = version.version
__licence__ = version.licence
del version

#    Copyleft (C) 2008 Acness World
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

import socket
import urllib2
import os

# ==============================================================================
# Public functions
# ==============================================================================

# ------------------------------------------------------------------------------
# Check the internet connection.
# ------------------------------------------------------------------------------
def URLCheckConnection():
    """Check the internet connection.
    @return: The internet connection state.
    """
    # Save the old default connection timeout
    old_timeout = socket.getdefaulttimeout()
    # Set the default connection timeout
    socket.setdefaulttimeout(10.)
    # Initialize the result dictionary
    result = True
    # Attempt to connect to the google web site
    try:
        f = urllib2.urlopen("http://www.google.com")
        f.close()
    except urllib2.HTTPError, exc:
        result = False
    except urllib2.URLError, exc:
        result = False
    except:
        result = False
    # Restore the old default connection timeout
    socket.setdefaulttimeout(old_timeout)
    # Return the result
    return result

# ------------------------------------------------------------------------------
# Retrieve informations from url.
# ------------------------------------------------------------------------------
def URLGetInfos(url, timeout = 5.0):
    """Retrieve informations from url.
    @param url: URL.
    @param timeout: Connection timeout.
    @return: Informations as dictionary or None.
             ['Last-Modified', 'Content-Length']
    """
    # Save the old default connection timeout
    old_timeout = socket.getdefaulttimeout()
    # Set the default connection timeout
    socket.setdefaulttimeout(timeout)
    # Initialize the result dictionary
    result = {
        "Last-Modified" : "",
        "Content-Length" : ""
    }
    # Attempt to retrieve the url headers
    try:
        f = urllib2.urlopen(url)
        try:
            result["Last-Modified"] = f.info().getheader("Last-Modified")
            result["Content-Length"] = f.info().getheader("Content-Length")
        except:
            result = None
        f.close()
    except urllib2.HTTPError, exc:
        result = None
    except urllib2.URLError, exc:
        result = None
    except:
        result = None
    # Restore the old default connection timeout
    socket.setdefaulttimeout(old_timeout)
    # Return the result
    return result

# ------------------------------------------------------------------------------
# Download a file from an URL to a string.
# ------------------------------------------------------------------------------
def URLDownloadToString(url, timeout = 5.0):
    """Download a file from an URL to a string.
    @param url: URL.
    @param timeout: Connection timeout.
    @return: The data as string or None.
    """
    # Save the old default connection timeout
    old_timeout = socket.getdefaulttimeout()
    # Set the default connection timeout
    socket.setdefaulttimeout(timeout)
    # Initialize the result
    result = ''
    # Attempt to download the file
    try:
        f = urllib2.urlopen(url)
        try:
            result = f.read()
        except:
            result = None
        f.close()
    except urllib2.HTTPError, exc:
        result = None
    except urllib2.URLError, exc:
        result = None
    except:
        result = None
    # Restore the old default connection timeout
    socket.setdefaulttimeout(old_timeout)
    # Return the result
    return result

# ------------------------------------------------------------------------------
# Download a file from an URL.
# ------------------------------------------------------------------------------
def URLDownloadToFile(url, filePath, timeout = 5.0):
    """Download a file from an URL.
    @param url: URL of the file.
    @param filePath: Output file path.
    @param timeout: Connection timeout.
    @return: The success result.
    """
    result = True
    fs = URLDownloadToString(url, timeout)
    if fs != None:
        try:
            f = open(filePath, 'wb')
            try:
                f.write(fs)
            except:
                result = False
            f.close()
        except:
            result = False
    else:
        result = False
    return result
