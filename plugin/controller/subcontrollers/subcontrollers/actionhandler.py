
from qgis.core import *
from qgis.gui import *
from qgis.PyQt.QtCore import *

################################################################################
### Imports
################################################################################

# Action indices
from .actionmanager import ACTION
from .sessionmenu import SessionMenu as MENU

# ActionHandler handles actions for Sessions and Markers
from .subcontrollers import SessionController
from .subcontrollers import MarkersController

################################################################################

class ActionHandler:
    def __init__(self, iface):
        self._iface = iface
        self._sessionController = None
        self._markersController = None

    @property
    def sessionController(self):
        if not self._sessionController:
            self._sessionController = SessionController(self._iface)
        return self._sessionController

    @property
    def markersController(self):
        if not self._markersController:
            self._markersController = MarkersController(self._iface)
        return self._markersController

    ########################################################################
    ### Update Action
    ########################################################################

    def updateAction(self, action, idx):
        print('ActionHandler.updateAction', action.text(), idx)
        return self.markersController.updateAction(action, idx)

    def updateMenuAction(self, sender, action, idx):
        print('ActionHandler.updateMenuAction', action.text(), idx)
        return self.sessionController.updateAction(action, idx)

    ########################################################################
    ### Handle Action
    ########################################################################

    def handleAction(self, sender, idx):
        return self.markersController.handleAction(sender, idx)

    def handleMenuAction(self, sender, action, idx):
        return self.sessionController.handleAction(sender, idx)
