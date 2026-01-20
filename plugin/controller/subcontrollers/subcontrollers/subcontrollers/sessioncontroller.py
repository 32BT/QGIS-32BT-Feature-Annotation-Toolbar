

from qgis.core import *
from qgis.gui import *
from qgis.PyQt.QtCore import *


################################################################################
### Imports
################################################################################

# Action indices
from ..actionmanager import ACTION



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
        return idx == ACTION.INDEX.RESET

    def handleAction(self, sender, idx):
        if idx == ACTION.INDEX.RESET:
            return self.startSession()

    def startSession(self):
        print('SessionController.startSession')
