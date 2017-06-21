# -*- coding: latin1 -*-

"""
tuxisalive
==========

    Python utilities for Tuxdroid from the kysoh compagny. 
    
    http://www.tuxisalive.com
"""

import version
__name__ = version.name
__author__ = version.author
__date__ = version.date
__version__ = version.version
__licence__ = version.licence
del version

#    Copyright (C) 2008 C2ME Sa
#    Rémi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

#
# tuxisalive package modules
#
import api
try:
    import lib
except:
    pass