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

def checkValue(value, rType, lower = None, upper = None):
    """Check the type and boundaries of a value.
    """
    # Get the type of the value to check
    vType = str(type(value))
    vType = vType[vType.find("'")+1:vType.rfind("'")]
    # Check the type of the value
    if vType != rType:
        print "Invalid type : '%s' != '%s'" % (vType, rType)
        return False
    # Check the bounds of the value
    if vType in ['int', 'float']:
        if lower != None:
            if value < lower:
                return False
        if upper != None:
            if value > upper:
                return False

    return True