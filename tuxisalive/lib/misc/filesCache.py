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

try:
    from hashlib import md5
except:
    from md5 import md5

if os.name == 'nt':
    import win32con
    import win32file

from urlTools import getUrlInfo, downloadUrlToStream
import directoriesAndFiles

_BASE_TEMP_DIR = directoriesAndFiles.getTmpPath()


def getMD5HashOfURI(uri):
    """Get the MD5 hash code from some informations of a file.
    @param uri: File location.
    @return: The MD5 hash code.
    """
    result = ""
    md5H = md5()
    fileName = ""
    # Check if the file is on the hard drive
    if os.path.isfile(uri):
        len = os.path.getsize(uri)
        lastMod = os.path.getmtime(uri)
        fileName = os.path.basename(uri)
        md5H.update(fileName + str(lastMod) + str(len))
        result = md5H.hexdigest()
    else:
        if (uri.lower().find("http://") == 0) or \
            (uri.lower().find("https://") == 0) or \
            (uri.lower().find("ftps://") == 0) or \
            (uri.lower().find("ftp://") == 0):
            ret, info = getUrlInfo(uri)
            if ret:
                len = info["Content-Length"]
                lastMod = info["Last-Modified"]
                fileName = os.path.basename(uri)
                md5H.update(fileName + lastMod + len)
                result = md5H.hexdigest()

    return result

class CachedFile(object):
    """Class to make a virtual cached file.
    """

    def __init__(self, uri, cachePrefix = "kysohcf"):
        """Constructor of cached file object.
        @param uri: Input file location.
        @param cachePrefix: Cache directory location.
        """
        self.__isValid = True
        self.__cacheDir = os.path.join(_BASE_TEMP_DIR, cachePrefix)
        if not os.path.isdir(self.__cacheDir):
            directoriesAndFiles.createDirs(self.__cacheDir)
        self.__uri = uri
        self.__md5Tag = getMD5HashOfURI(uri)
        if self.__md5Tag == "":
            self.__isValid = False
            return
        self.__outputPath = self.__generateOutputFileName()
        if not self.__writeOutputFile():
            self.__isValid = False
            return

    def __generateOutputFileName(self):
        """Generate the output file name in the cache.
        """
        extension = ""
        extension_idx = self.__uri.lower().rfind(".")
        if extension_idx != -1:
            extension = self.__uri[extension_idx:]
        outputPath = os.path.join(self.__cacheDir, self.__md5Tag)
        outputPath = "%s%s" % (outputPath, extension)
        return outputPath

    def __writeOutputFile(self):
        """Copy the source file to the cache.
        """
        try:
            fo = open(self.__outputPath, "wb")
        except:
            return False

        # If file from internet
        if (self.__uri.lower().find("http://") == 0) or \
           (self.__uri.lower().find("https://") == 0) or \
           (self.__uri.lower().find("ftps://") == 0) or \
           (self.__uri.lower().find("ftp://") == 0):
            success, stream = downloadUrlToStream(self.__uri)
            if success:
                fo.write(stream)
                fo.close()
            else:
                fo.close()
                return False
        # File from hard drive
        else:
            if not os.path.isfile(self.__uri):
                fo.close()
                return False
            else:
                try:
                    fi = open(self.__uri, "rb")
                    fo.write(fi.read())
                    fi.close()
                    fo.close()
                except:
                    fo.close()
                    return False
        return True

    def getOutputFilePath(self):
        """Get the output file path.
        """
        if not self.__isValid:
            return ""
        return self.__outputPath

    def getSourceUri(self):
        """Get the uri source.
        """
        return self.__uri

    def getValid(self):
        """Get the validity of the cached file.
        """
        return self.__isValid

    def getMd5Tag(self):
        """Get the Md5 hash tag.
        """
        if not self.__isValid:
            return ""
        return self.__md5Tag

    def destroy(self):
        """Destroy the cached file.
        """
        directoriesAndFiles.removeFile(self.__outputPath)
        self.__isValid = False

class CachedFilesContainer(object):
    """Class to make a container of virtual cached files.
    """

    def __init__(self, cachePrefix = "kysohcf"):
        """Constructor of container of cached files object.
        @param cachePrefix: Cache directory location.
        """
        self.__cachePrefix = cachePrefix
        self.__cacheDir = os.path.join(_BASE_TEMP_DIR, self.__cachePrefix)
        directoriesAndFiles.createDirsF(self.__cacheDir)
        self.__container = []

    def getCacheDir(self):
        """Get the cache directory.
        @return: The cache directory path.
        """
        return self.__cacheDir

    def __checkUriInCacheExists(self, uri):
        """Check if a uri already exists in the cache.
        """
        md5Tag = getMD5HashOfURI(uri)
        for cFile in self.__container:
            if (cFile.getMd5Tag() == md5Tag) and \
               (cFile.getMd5Tag() != ""):
                return cFile
        return None

    def createFileCache(self, uri):
        """Create a cached file.
        @param uri: File location.
        @return: A CachedFile object.
        """
        result = self.__checkUriInCacheExists(uri)
        if result == None:
            result = CachedFile(uri, self.__cachePrefix)
            if result.getValid():
                self.__container.append(result)
            else:
                result = None
        return result

    def destroyFileCache(self, cachedFile):
        """Destroy a cached file.
        @param cachedFile: CachedFile object.
        """
        if cachedFile == None:
            return
        for i, cFile in enumerate(self.__container):
            if cFile.getMd5Tag() == cachedFile.getMd5Tag():
                cachedFile.destroy()
                self.__container.pop(i)
                break

    def destroy(self):
        """Destroy the cached files container object.
        """
        directoriesAndFiles.removeDirs(self.__cacheDir)
        self.__container = []
