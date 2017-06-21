# -*- coding: utf-8 -*-

"""
Util
====

    Utilities module.

    http://www.tuxisalive.com
"""

from tuxisalive.lib.Util import version
__name__ = version.name
__author__ = version.author
__date__ = version.date
__version__ = version.version
__licence__ = version.licence
del version

#    Copyleft (C) 2008 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

#
# Util package modules
#
from tuxisalive.lib.Util.DirectoriesAndFilesTools import *
from tuxisalive.lib.Util.XMLSerializer import *
from tuxisalive.lib.Util.URLTools import *
from tuxisalive.lib.Util.FilesCache import *
