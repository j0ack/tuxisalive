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

import os
import subprocess
import time

# Error codes enumeration.
E_TUXUP_NOERROR                 = 0
E_TUXUP_CMDNOTFOUND             = 1
E_TUXUP_BADPARAMETER            = 2
E_TUXUP_DONGLENOTFOUND          = 3
E_TUXUP_DONGLEMANUALBOOTLOAD    = 4
E_TUXUP_BADPROGFILE             = 5
E_TUXUP_BOOTLOADINGFAILED       = 6
E_TUXUP_USBERROR                = 7
E_TUXUP_DFUPROGNOTFOUND         = 8
E_TUXUP_PROGRAMMINGFAILED       = 9
E_TUXUP_FUXUSBVERERROR          = 10

E_CODE_LIST = [
    E_TUXUP_NOERROR,
    E_TUXUP_CMDNOTFOUND,
    E_TUXUP_BADPARAMETER,
    E_TUXUP_DONGLENOTFOUND,
    E_TUXUP_DONGLEMANUALBOOTLOAD,
    E_TUXUP_BADPROGFILE,
    E_TUXUP_BOOTLOADINGFAILED,
    E_TUXUP_USBERROR,
    E_TUXUP_DFUPROGNOTFOUND,
    E_TUXUP_PROGRAMMINGFAILED,
    E_TUXUP_FUXUSBVERERROR,
]

E_STR_LIST = [
    "No error",
    "Tuxup not found",
    "Bad parameter",
    "Dongle not found",
    "The dongle must be manually bootloaded",
    "Bad (*.hex or *.eep) file",
    "Bootloading failed",
    "USB error",
    "Dfu-programmer not found",
    "Programming failed",
    "Fuxusb bad version"
]

DFU_CMD_GET = [
    "dfu-programmer",
    "at89c5130",
    "get",
    "bootloader-version",
]

DFU_CMD_ERASE = [
    "dfu-programmer",
    "at89c5130",
    "erase",
]

DFU_CMD_FLASH = [
    "dfu-programmer",
    "at89c5130",
    "flash",
    "<filename>",
]

DFU_CMD_CONFIGURE = [
    "dfu-programmer",
    "at89c5130",
    "configure",
    "HSB",
    "0x7b",
]

DFU_CMD_START = [
    "dfu-programmer",
    "at89c5130",
    "start",
]

class Tuxup(object):
    """Wrapper class to tuxup.
    """

    def __execute(self, cmd = []):
        """
        """
        if len(cmd) < 1:
            return E_TUXUP_CMDNOTFOUND
        p = subprocess.Popen(cmd,
                             stdout = subprocess.PIPE,
                             stdin = subprocess.PIPE,
                             stderr = subprocess.PIPE)
        return p.wait()

    def __checkTuxupFound(self):
        """
        """
        ret = self.__execute(["tuxup",])
        if ret == E_TUXUP_CMDNOTFOUND:
            return False
        else:
            return True

    def exists(self):
        """Check that the tuxup application exists.
        @return: True or False
        """
        return self.__checkTuxupFound()

    def flashOne(self, fileName):
        """Flash one file with tuxup.
        @param fileName: file name to flash (*.hex|*.eep)
        @return: the error code
        """
        cmd = [
            "tuxup",
            fileName,
        ]
        p, key = os.path.split(fileName)
        ret = self.__execute(cmd)
        return ret

    def __flashOneTimeout(self, fileName, attemptNumber = 10):
        """
        """
        ret = E_TUXUP_NOERROR
        count = 0
        while True:
            ret = self.flashOne(fileName)
            if (ret == E_TUXUP_DONGLENOTFOUND) or \
                (ret == E_TUXUP_PROGRAMMINGFAILED):
                time.sleep(1)
            elif ret == E_TUXUP_NOERROR:
                break
            count += 1
            if count == attemptNumber:
                break
        return ret

    def flashUSBManually(self, fileName):
        """Flash the usb cpu after you have manually switched the dongle
        to the bootloader mode (With the button at the bottom).
        This command will force to flash with the input file.
        No verification is made except the file name which must be
        "fuxusb.hex".
        @param fileName: file name of the usb firmware
        @return: the error code
        """

        # Check that the dongle found and it is in
        # bootloader mode.
        ret = self.__execute(DFU_CMD_GET)
        if ret != E_TUXUP_NOERROR:
            return E_TUXUP_DONGLENOTFOUND

        # Check that the input file exists
        if not os.path.isfile(fileName):
            return E_TUXUP_BADPROGFILE

        # Check that the input file is "fuxusb.hex"
        if fileName.find("fuxusb.hex") == -1:
            return E_TUXUP_BADPROGFILE

        # Erase the usb cpu memory flash
        ret = self.__execute(DFU_CMD_ERASE)
        if ret != E_TUXUP_NOERROR:
            return E_TUXUP_PROGRAMMINGFAILED

        # Transfer the firmware in the usb cpu memory flash
        DFU_CMD_FLASH[3] = fileName
        ret = self.__execute(DFU_CMD_FLASH)
        if ret != E_TUXUP_NOERROR:
            return E_TUXUP_PROGRAMMINGFAILED

        # Configure HSB
        ret = self.__execute(DFU_CMD_CONFIGURE)
        if ret != E_TUXUP_NOERROR:
            return E_TUXUP_PROGRAMMINGFAILED

        # Exit the bootloader mode
        ret = self.__execute(DFU_CMD_START)
        if ret != E_TUXUP_NOERROR:
            return E_TUXUP_PROGRAMMINGFAILED

        return ret

    def flashMany(self, fileNames):
        """Flash many files with tuxup.
        @param fileNames: list of the files to flash (*.hex|*.eep)
        @return: the error codes list in a Dict object
        """
        result = {}
        for fileName in fileNames:
            p, key = os.path.split(fileName)
            result[key] = E_TUXUP_NOERROR
        for i, fileName in enumerate(fileNames):
            if i == 0:
                ret = self.flashOne(fileName)
            else:
                ret = self.__flashOneTimeout(fileName)
            p, key = os.path.split(fileName)
            result[key] = ret
            if ret != E_TUXUP_NOERROR:
                break
        return result

    def strError(self, errorCode):
        """Return the string of an error code.
        @param errorCode: error code
            E_CODE_LIST = [
                E_TUXUP_NOERROR,
                E_TUXUP_CMDNOTFOUND,
                E_TUXUP_BADPARAMETER,
                E_TUXUP_DONGLENOTFOUND,
                E_TUXUP_DONGLEMANUALBOOTLOAD,
                E_TUXUP_BADPROGFILE,
                E_TUXUP_BOOTLOADINGFAILED,
                E_TUXUP_USBERROR,
                E_TUXUP_DFUPROGNOTFOUND,
                E_TUXUP_PROGRAMMINGFAILED,
                E_TUXUP_FUXUSBVERERROR,
            ]
        @return: a string.
        """
        if not errorCode in E_CODE_LIST:
            return "Unknow error"
        else:
            return E_STR_LIST[errorCode]