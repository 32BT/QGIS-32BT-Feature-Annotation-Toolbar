

from qgis.core import *
from qgis.gui import *
from qgis.PyQt.QtCore import *


################################################################################
### Imports
################################################################################

# Menu indices
from ..sessionmenu import SessionMenu as MENU

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

    def validateStartSession(self):
        return True

    def handleAction(self, sender, idx):
        if idx == MENU.ITEM.INDEX.START_SESSION:
            return self.startSession()

    def startSession(self):
        print('SessionController.startSession')

