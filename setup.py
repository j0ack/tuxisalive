#!/usr/bin/env python
# -*- coding: latin1 -*-

from distutils.sysconfig import *
from distutils.core import setup
from glob import glob
import os
import sys 

os.environ['PYTHONHOME']='/usr'
get_python_lib()
#
# Check dependencies
#
packageDependencies = [
    'xml.dom.minidom',
    'httplib',
    'zipfile',
    'urllib2',
    'socket',
    'threading',
    'copy',
    'BaseHTTPServer',
    'SocketServer',
    're',
    'urllib',
    'ctypes',
]

if os.name == 'nt':
    packageDependencies.append('pyHook')
    packageDependencies.append('pythoncom')
    
for moduleName in packageDependencies:
    try:
        print "check module presence (%s)" % moduleName
        exec("import %s" % moduleName) in globals()
        exec("del %s" % moduleName) in globals()
    except:
        print "ERROR : Module (%s) not found !" % moduleName
        sys.exit(-1)
        
#
# Packages list
#
mPackages = [
    'tuxisalive', 
    'tuxisalive.api', 
    'tuxisalive.lib',
    'tuxisalive.lib.driver',
    'tuxisalive.lib.osl',
    'tuxisalive.lib.httpserver',
    'tuxisalive.lib.logger',
    'tuxisalive.lib.daemonizer',
    'tuxisalive.lib.tuxup',
    'tuxisalive.lib.misc',
    'tuxisalive.lib.attitunes',
    'tuxisalive.lib.IPN',
    'tuxisalive.lib.Util',
]

if os.name == 'nt':
    mPackages.append('tuxisalive.lib.wordlogger')

#
# Install the package (python files only)
#
PACKAGE_BASE_PATH = get_python_lib()

setup(name = 'tuxisalive',
      version = '0.2.1',
      description = 'Python utilities for Tuxdroid',
      author = 'Remi Jocaille',
      author_email = 'remi.jocaille@c2me.be',
      url = 'http://www.tuxisalive.com',
      packages = mPackages,
      )

# Some distro (like OpenSUSE) install the site-package on /usr/local/lib/...
# but install the data files on /usr/lib/...
# If the .so files are not located with the site-package installation, they're
# not found, and the server wont start.
# To prevent this problem, installation is made three steps :
# - 1st : python file installation on the standard location.
# - 2nd : verify if the installation had been made on /usr/lib or /usr/local/lib
# - 3rd : change the path if needed, and install the .so libraries on the
#         correct place.

# XXX I'm not sure that trick will works on Windows.
if os.name != 'nt':
    # Test if tuxisalive has been installed on /usr/local/lib/...
    if  os.system("test -d /usr/local/lib/python2.5/site-packages/tuxisalive") == 0:
        # Change the installation PATH for the .so libraries.
        PACKAGE_BASE_PATH = "/usr/local/lib/python2.5/site-packages"

#
# Install the package (.so files only)
#
setup(name = 'tuxisalive',
      version = '0.2.1',
      description = 'Python utilities for Tuxdroid',
      author = 'Remi Jocaille',
      author_email = 'remi.jocaille@c2me.be',
      url = 'http://www.tuxisalive.com',
      data_files = [
          (PACKAGE_BASE_PATH + '/tuxisalive/lib/driver', 
            ['tuxisalive/lib/driver/libtuxdriver.dll', 
             'tuxisalive/lib/driver/libtuxdriver.so']),
          (PACKAGE_BASE_PATH + '/tuxisalive/lib/osl', 
            ['tuxisalive/lib/osl/libtuxosl.dll', 
             'tuxisalive/lib/osl/libtuxosl.so']),
      ]    
      )
