

################################################################################
### Imports
################################################################################

# Require FSItem for user-relative paths
from .controller.subcontrollers.subcontrollers.subcontrollers.database import FSItem

################################################################################

# Require MODULE identity for section/groupnames in settingsfile
import sys
_MODULE = sys.modules.get(__name__.split('.')[0])
_AUTHOR = _MODULE.identity.AUTHOR
_MODULE = _MODULE.identity.MODULE

################################################################################
### Settings
################################################################################

from qgis.core import QgsSettings

class Settings(QgsSettings):
    @staticmethod
    def getGlobalValue(key):
        with Settings() as settings:
            return settings.loadValue(key)
    @staticmethod
    def setGlobalValue(key, value):
        with Settings() as settings:
            settings.saveValue(key, value)


    def __enter__(self):
        # start with group '32bt' which will create a section [32bt]
        # (add section=self.Plugins if it needs to go in section [plugins])
        self.beginGroup(_AUTHOR)
        self.beginGroup(_MODULE)
        return self

    def __exit__(self, *args):
        self.endGroup()
        self.endGroup()
        self.sync()

    ########################################################################
    # save dictionary k,v pairs under groupname key
    def saveGroup(self, key, dct):
        self.remove(key)
        self.beginGroup(key)
        try:
            self.saveGroupValues(dct)
        finally:
            self.endGroup()

    def loadGroup(self, key):
        self.beginGroup(key)
        try:
            return self.loadGroupValues()
        finally:
            self.endGroup()

    ########################################################################

    def saveGroupValues(self, dct):
        for key,val in dct.items():
            if isinstance(val, dict):
                self.saveGroup(key, val)
            else:
                self.saveValue(key, val)

    def loadGroupValues(self):
        D = {}
        for key in self.childKeys():
            D[key] = self.loadValue(key)
        for key in self.childGroups():
            D[key] = self.loadGroup(key)
        return D

    ########################################################################
    def savePath(self, key, path):
        self.saveValue(key, FSItem.path_shrinkuser(path))

    def loadPath(self, key):
        return FSItem.path_expanduser(self.loadValue(key))
    ########################################################################
    def saveValue(self, key, val):
        self.setValue(key,val)

    def loadValue(self, key):
        return self.value(key, '')
    ########################################################################
