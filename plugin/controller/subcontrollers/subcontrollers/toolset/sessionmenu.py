

from qgis.core import *
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtWidgets import *
from qgis.PyQt.QtGui import *

################################################################################
### Definitions
################################################################################
'''
'''
class MENU:
    class BUTTON:
        INDEX                = -1
    class ITEM:
        class INDEX:
            SESSION          = 0
            SETTINGS         = 1
            SESSION_START    = 2

################################################################################
### Language
################################################################################

import sys
_MODULE = sys.modules.get(__name__.split('.')[0])
_IDENTITY = _MODULE.IDENTITY
_LANGUAGE = _MODULE.LANGUAGE
_LABELS = _LANGUAGE.LABELS({
    "SESSIONMENU": {
        "TITLE": "Sessionmenu",
        "ITEM1": "Session",
        "ITEM2": "Settings..." },
    "STARTMENU": {
        "TITLE": "Session",
        "ITEM1": "Start..." }
    })


################################################################################
### SessionMenu
################################################################################

class SessionMenu(QMenu, MENU):
    updateAction = pyqtSignal(object, object, object)
    handleAction = pyqtSignal(object, object, object)

    def __init__(self, parent=None):
        super().__init__(_LABELS.SESSIONMENU.TITLE, parent)
        self.setObjectName("fat:sessionMenu")

        self._actions = []

        self._startMenu = StartMenu(_LABELS.STARTMENU.TITLE)
        action = self.addMenu(self._startMenu)
        action.setObjectName("fat:menuActionStartMenu")
        self._actions.append(action)

        action = self.addSeparator()

        action = self.addAction(_LABELS.SESSIONMENU.ITEM2)
        action.setObjectName("fat:menuActionSettings")
        self._actions.append(action)

        self.aboutToShow.connect(self.updateActions)
        self.triggered.connect(self.actionTriggered)


    def action(self, idx):
        if idx < len(self._actions):
            return self._actions[idx]
        else:
            idx -= len(self._actions)
            return self._startMenu.actions()[idx]

    ########################################################################

    def updateActions(self):
        self._startMenu.updateMenu()
        actions = self._actions + self._startMenu.actions()
        for idx, action in enumerate(actions):
            self.emitUpdate(action, idx)

    def actionTriggered(self, action):
        actions = self._actions + self._startMenu.actions()
        if action in actions:
            idx = actions.index(action)
            self.emitAction(action, idx)

    ########################################################################
    def emitUpdate(self, action, idx):
        self.updateAction.emit(self, action, idx)

    def emitAction(self, action, idx):
        self.handleAction.emit(self, action, idx)
    ########################################################################

################################################################################
### Start Menu
################################################################################
'''
WARNING: SessionController is part of ..subcontrollers.__init__ and refers back
to this file for the MENU definition.
This does not seem to cause problems THE FIRST TIME loading the plugin, but it
does cause problems on subsequent activations if sessioncontroller tries to read
beyond the database import. BEWARE WHEN TESTING!

Triple safety measures:
    - MENU is defined first
    - SessionMenu includes MENU
    - StartMenu is defined after SessionMenu
'''
from ..subcontrollers.database import Database

class StartMenu(QMenu):
    class ITEM:
        class INDEX:
            START = 0

    def updateMenu(self):
        self.clear()
        self.addAction(_LABELS.STARTMENU.ITEM1)
        db = Database()
        if db and db.exists():
            sessionSet = db.getSessionSet()
            items = list(sessionSet.folderItemNames())
            for item in items:
                action = self.addAction(item)
                action.setData(sessionSet.itemPath(item))




