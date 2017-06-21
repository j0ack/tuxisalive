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

import os
import shutil

if os.name == 'nt':
    import win32con
    import win32file

def removeDirsFilter(path, filters = ['.pyc', '.pyo']):
    """Remove directories and files recursively.

    @param path: path of the base directory.
    """
    def checkFilter(name):
        for filter in filters:
            if name.lower().find(filter) != -1:
                return True
        return False

    if not os.path.isdir(path):
        return

    for root, dirs, files in os.walk(path, topdown = False):
        for d in dirs:
            if checkFilter(os.path.join(root, d)):
                try:
                    os.removedirs(os.path.join(root, d))
                except:
                    pass
        for f in files:
            if checkFilter(os.path.join(root, f)):
                try:
                    if os.name == 'nt':
                        win32file.SetFileAttributesW(os.path.join(root, f),
                            win32con.FILE_ATTRIBUTE_NORMAL)
                    os.remove(os.path.join(root, f))
                except:
                    pass

def removeFile(filePath):
    """Remove a file.

    @param filePath: File path.
    """
    if os.path.isfile(filePath):
        try:
            if os.name == 'nt':
                win32file.SetFileAttributesW(filePath,
                    win32con.FILE_ATTRIBUTE_NORMAL)
            os.remove(filePath)
        except:
            pass

def removeDirs(path):
    """Remove directories and files recursively.

    @param path: path of the base directory.
    """
    if not os.path.isdir(path):
        return

    for root, dirs, files in os.walk(path, topdown = False):
        for d in dirs:
            try:
                os.removedirs(os.path.join(root, d))
            except:
                pass
        for f in files:
            try:
                if os.name == 'nt':
                    win32file.SetFileAttributesW(os.path.join(root, f),
                        win32con.FILE_ATTRIBUTE_NORMAL)
                os.remove(os.path.join(root, f))
            except:
                pass

    if os.path.isdir(path):
        try:
            os.removedirs(path)
        except:
            pass

def createDirs(path):
    """Force to create a directories tree if not exists.

    @param path: directory tree.
    """
    if not os.path.isdir(path):
        os.makedirs(path)

def createDirsF(path):
    """Force to create a directories tree after having deleted the old one.

    @param path: directory tree.
    """
    if os.path.isdir(path):
        removeDirs(path)
    os.makedirs(path)

def copyDir(src, dest):
    """Copy a directories tree to another directory.

    @param src: source path.
    @param dest: destination path.
    """
    if not os.path.isdir(src):
        return
    createDirs(dest)
    if os.path.isdir(dest):
        removeDirs(dest)
    shutil.copytree(src, dest)

def getTmpPath():
    """Retrieve the os Tempporary path.
    """
    result = None
    # On Windows
    if os.name == 'nt':
        result = os.environ.get('tmp')
        if result == None:
            result = os.environ.get('temp')
            if result == None:
                result = "c:\\windows\\temp"
    # On linux
    else:
        result = "/tmp"
    return result