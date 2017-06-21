# -*- coding: latin1 -*-

"""
Misc
====

    Miscelleanous libraries for Tuxdroid.

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
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

#
# misc package modules
#
from tuxisalive.lib.misc.directoriesAndFiles import *
from tuxisalive.lib.misc.urlTools import *
from tuxisalive.lib.misc.filesCache import *
from tuxisalive.lib.misc.SimpleXMLStruct import *
from tuxisalive.lib.misc.tuxPaths import *
