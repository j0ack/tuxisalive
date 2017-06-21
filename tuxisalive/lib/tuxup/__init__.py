# -*- coding: latin1 -*-

"""
Tuxup
=========

    Tuxup is a wrapper to the USB flasher utility.

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
# Tuxup package modules
#
from tuxisalive.lib.tuxup.Tuxup import *