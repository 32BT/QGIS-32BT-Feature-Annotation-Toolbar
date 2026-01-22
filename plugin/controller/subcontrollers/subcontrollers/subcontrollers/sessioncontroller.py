
import os

from qgis.core import *
from qgis.gui import *
from qgis.PyQt.QtCore import *


################################################################################
### Imports
################################################################################

# Menu definitions
from ..toolset.sessionmenu import SessionMenu as MENU

from .database import Database
from .dialogs import StorageDialog
from .dialogs import SessionDialog
from .tms.session import Session

################################################################################
### Language
################################################################################

import sys
_MODULE = sys.modules.get(__name__.split('.')[0])
_LABELS = _MODULE.LANGUAGE.LABELS({})

################################################################################
### Controller
################################################################################

class SessionController:
    def __init__(self, iface):
        self._iface = iface

    ########################################################################
    ### Update Action
    ########################################################################

    def updateAction(self, action, idx):
        action.setEnabled(self.validateAction(action, idx))

    def validateAction(self, action, idx):
        if idx == MENU.BUTTON.INDEX:
            return True
        if idx == MENU.ITEM.INDEX.START_SESSION:
            return self.validateActionStartSession()
        if idx == MENU.ITEM.INDEX.STORAGE_LOCATION:
            return self.validateActionStorageLocation()

    def validateActionStartSession(self):
        return True

    def validateActionStorageLocation(self):
        return True

    ########################################################################
    ### Handle Action
    ########################################################################

    def handleAction(self, sender, idx):
        if idx == MENU.ITEM.INDEX.START_SESSION:
            return self.startSession()
        if idx == MENU.ITEM.INDEX.STORAGE_LOCATION:
            return self.askStorageLocation()

    def startSession(self):
        path = self.getStorageLocation()
        if path:
            sessionSet = Database(path).getSessionSet()
            name = self.askSessionName(sessionSet)
            if name:
                path = sessionSet.itemPath(name)
                layer = Session(path).start_layer()
                self._iface.setActiveLayer(layer)

    ########################################################################
    ### Storage Location
    ########################################################################

    def getStorageLocation(self):
        path = Database.getGlobalPath()
        if not path or not os.path.exists(path):
            path = self.askStorageLocation(path)
        return path

    def askStorageLocation(self, path=None):
        parent = self._iface.mainWindow()
        path = path or Database.getGlobalPath()
        path = StorageDialog(parent).askStorageLocation(path)
        if path:
            Database.setGlobalPath(path)
            return path

    ########################################################################

    def askSessionName(self, sessionSet):
        parent = self._iface.mainWindow()
        return SessionDialog(parent).askInput(sessionSet)
