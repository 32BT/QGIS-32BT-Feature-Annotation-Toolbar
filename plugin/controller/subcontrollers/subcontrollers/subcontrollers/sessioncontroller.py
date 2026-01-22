
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
from .tms.sentinel import Sentinel

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
        # Listen for incomming sessionlayers
        self._sentinel = Sentinel()

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

    # Setting the central storagelocation is always possible
    def validateActionStorageLocation(self):
        return True

    # Annotations are only useful if there is something to annotate...
    def validateActionStartSession(self):
        return len(QgsProject.instance().mapLayers())>0

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
    '''
    Starting a Session requires a central storage location. If it was not
    previously set, then we need to first ask for a central storage location.
    '''
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
    '''
    Only option currently is a name for a folder (in the  sessionSet folder).
    If name refers to an existing folder, then items will be appended to that
    existing folder. If name is new, then a new folder will be created.

    Folder hierarchy is:

        /Centralstorage         (selected by user)
            /sessions           (sessionSet folder, created by Database)
                /<name>         (user input)
                    /markers    (new markers are stored here)
                    /archive    (deleted markers are stored here)
    '''
    def askSessionName(self, sessionSet):
        parent = self._iface.mainWindow()
        return SessionDialog(parent).askInput(sessionSet)
