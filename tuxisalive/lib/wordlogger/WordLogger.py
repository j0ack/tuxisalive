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

import pyHook
import time
import pythoncom
import threading

from tuxisalive.api.TuxEventHandler import TuxEventHandler

CUT_KEYS = [
    13,
    32,
]

class WordLogger(object):
    """Class the create a word logger.
    Only available for Windows.
    """

    def __init__(self):
        """Constructor of the class.
        """
        self.__hm = pyHook.HookManager()
        self.__hm.KeyDown = self.__OnKeyboardEvent
        self.__hm.HookKeyboard()
        self.__started = False
        self.__startedMutex = threading.Lock()
        self.__currentWord = ""
        self.handler = TuxEventHandler()

    def destroy(self):
        """Destructor of the class.
        """
        self.stop()

    def __setStarted(self, value):
        """
        """
        self.__startedMutex.acquire()
        self.__started = value
        self.__startedMutex.release()

    def __getStarted(self):
        """
        """
        self.__startedMutex.acquire()
        value = self.__started
        self.__startedMutex.release()
        return value

    def __poolLoop(self):
        """
        """
        self.__setStarted(True)
        while self.__getStarted():
            try:
                pythoncom.PumpWaitingMessages()
                time.sleep(0.01)
            except:
                time.sleep(0.01)

    def start(self):
        """Start the word logger.
        """
        if self.__getStarted():
            return
        self.__poolLoop()

    def stop(self):
        """Stop the word logger.
        """
        if not self.__getStarted():
            return
        self.__setStarted(False)
        self.__hm.UnhookKeyboard()

    def __OnKeyboardEvent(self, event):
        """
        """
        self.__processKey(event.Ascii)
        return True

    def __processKey(self, key):
        """
        """
        if (key == 32) or (key == 13) or (key == 46) or (key == 44):
            if len(self.__currentWord) > 0:
                self.handler.emit(self.__currentWord)
                self.__currentWord = ""
        elif key == 8:
            if len(self.__currentWord) > 0:
                self.__currentWord = self.__currentWord[:-1]
        elif key > 32:
            self.__currentWord = self.__currentWord + chr(key)
