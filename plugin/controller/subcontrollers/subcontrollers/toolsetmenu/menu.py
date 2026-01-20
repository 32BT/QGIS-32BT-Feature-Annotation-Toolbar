

from qgis.core import *
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtWidgets import *
from qgis.PyQt.QtGui import *


################################################################################
### Language
################################################################################

import sys
_MODULE = sys.modules.get(__name__.split('.')[0])
_IDENTITY = _MODULE.IDENTITY
_LANGUAGE = _MODULE.LANGUAGE
_LABELS = _LANGUAGE.LABELS({
    "SESSIONMENU_TITLE": "Sessionmenu",
    "SESSIONMENU_ITEM1": "Start Session"})

################################################################################
### SessionMenu
################################################################################

class SessionMenu(QMenu):

    ########################################################################
    ### Definities
    ########################################################################

    class BUTTON:
        INDEX                = -1
    class ITEM:
        class INDEX:
            START_SESSION    = 0

    ########################################################################

    updateAction = pyqtSignal(object, object, object)
    handleAction = pyqtSignal(object, object, object)

    def __init__(self, parent=None):
        super().__init__(_LABELS.SESSIONMENU_TITLE, parent)
        action = self.addAction(_LABELS.SESSIONMENU_ITEM1)

        self.aboutToShow.connect(self.updateActions)
        self.triggered.connect(self.actionTriggered)

    ########################################################################

    def updateActions(self):
        actions = self.actions()
        for idx, action in enumerate(actions):
            self.emitUpdate(action, idx)

    def actionTriggered(self, action):
        actions = self.actions()
        idx = actions.index(action)
        self.emitAction(action, idx)

    ########################################################################
    def emitUpdate(self, action, idx):
        self.updateAction.emit(self, action, idx)

    def emitAction(self, action, idx):
        self.handleAction.emit(self, action, idx)
    ########################################################################





