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

class TuxAPIAttitune(object):
    """Class to control the attitune files.
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
    
    def load(self, path):
        """Load an attitune file.
        
        @param path: path of the attitune file.
        @return: the success of the command.
        """
        if not checkValue(path, "str"):
            return False
        path = urllib.urlencode({'path' : path, })
        cmd = "attitune/load?%s" % path
        return self.__cmdSimpleResult(cmd)
    
    def play(self, begin = 0.0):
        """Play the loaded attitune.
        
        @param begin: starting second.
        @return: the success of the command.
        """
        if not checkValue(begin, "float"):
            return False
        cmd = "attitune/play?begin=%f" % begin
        return self.__cmdSimpleResult(cmd)
    
    def stop(self):
        """Stop the current attitune.
        
        @return: the success of the command.
        """
        cmd = "attitune/stop?"
        return self.__cmdSimpleResult(cmd)