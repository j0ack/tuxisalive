# -*- coding: latin1 -*-

import version
__author__ = version.author
__date__ = version.date
__version__ = version.version
__licence__ = version.licence
del version

#    Copyright (C) 2008 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

import socket
import urllib2

def getUrlInfo(url, timeout = 5.0):
    """Retrieve informations from url.
            ('Last-Modified', 'Content-Length')
    @param url: URL.
    @return: The success result and the informations as dictionary.
    """
    old_timeout = socket.getdefaulttimeout()
    socket.setdefaulttimeout(timeout)
    success = True
    result = {
        "Last-Modified" : "",
        "Content-Length" : ""
    }

    req = urllib2.Request(url)

    try:
        f = urllib2.urlopen(url)
    except urllib2.HTTPError, exc:
        success = False
    except urllib2.URLError, exc:
        success = False
    except:
        success = False

    if success:
        try:
            result["Last-Modified"] = f.info().getheader("Last-Modified")
            result["Content-Length"] = f.info().getheader("Content-Length")
            f.close()
        except:
            success = False

    socket.setdefaulttimeout(old_timeout)

    return success, result

def downloadUrlToStream(url, timeout = 5.0):
    """Download a file from an URL.
    @param url: URL.
    @return: The success result and the data stream.
    """
    old_timeout = socket.getdefaulttimeout()
    socket.setdefaulttimeout(timeout)
    success = True
    result = ''

    req = urllib2.Request(url)

    try:
        f = urllib2.urlopen(url)
    except urllib2.HTTPError, exc:
        success = False
    except urllib2.URLError, exc:
        success = False
    except:
        success = False

    if success:
        try:
            result = f.read()
            f.close()
        except:
            success = False

    socket.setdefaulttimeout(old_timeout)

    return success, result
