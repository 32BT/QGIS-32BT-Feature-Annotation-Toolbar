

from qgis.core import *
from qgis.gui import *
from qgis.PyQt.QtCore import *


################################################################################
### Imports
################################################################################

# Menu indices
from ..toolset.sessionmenu import SessionMenu as MENU

from .database import Database
from .dialogs import StorageDialog
from .dialogs import SessionDialog

################################################################################
### Language
################################################################################

import sys
_MODULE = sys.modules.get(__name__.split('.')[0])
_LABELS = _MODULE.LANGUAGE.LABELS({})


################################################################################

class SessionController:
    def __init__(self, iface):
        self._iface = iface

    def updateAction(self, action, idx):
        action.setEnabled(self.validateAction(action, idx))

    def validateAction(self, action, idx):
        if idx == MENU.BUTTON.INDEX:
            return self.validateStartSession()
        if idx == MENU.ITEM.INDEX.START_SESSION:
            return self.validateStartSession()
        if idx == MENU.ITEM.INDEX.STORAGE_LOCATION:
            return self.validateStorageLocation()

    def validateStartSession(self):
        return True

    def validateStorageLocation(self):
        return True

    def handleAction(self, sender, idx):
        if idx == MENU.ITEM.INDEX.START_SESSION:
            return self.startSession()
        if idx == MENU.ITEM.INDEX.STORAGE_LOCATION:
            return self.askStorageLocation()

    def startSession(self):
        print('SessionController.startSession')
        path = Database.getGlobalPath()
        path = path or self.askStorageLocation(path)
        if path:
            db = Database(path)
            sessionSet = None #db.getSessionSet()
            parent = self._iface.mainWindow()
            SessionDialog(parent).askSessionName(sessionSet)
            print(path)

    def askStorageLocation(self, path=None):
        parent = self._iface.mainWindow()
        path = path or Database.getGlobalPath()
        path = StorageDialog(parent).askStorageLocation(path)
        if path:
            Database.setGlobalPath(path)
            return path
