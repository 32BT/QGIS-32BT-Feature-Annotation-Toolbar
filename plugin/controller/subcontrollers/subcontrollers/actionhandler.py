
from qgis.core import *
from qgis.gui import *
from qgis.PyQt.QtCore import *

################################################################################
### Imports
################################################################################
'''
ActionHandler receives actions for both Sessions and Markers.
Session actions are a result of menuactions. (update/handleMenuAction)
Markers actions are a result of toolactions. (update/handleAction)
'''
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
    ### Handle Tool Actions (toolbar and contextmenu)
    ########################################################################
    '''
    Receives ACTION.INDEX types
    '''
    def updateAction(self, action, idx):
        return self.markersController.updateAction(action, idx)

    def handleAction(self, sender, idx):
        return self.markersController.handleAction(sender, idx)

    ########################################################################
    ### Handle Menu Actions (sessionmenu)
    ########################################################################
    '''
    Receives MENU.ITEM.INDEX types
    '''
    def updateMenuAction(self, sender, action, idx):
        return self.sessionController.updateAction(action, idx)

    def handleMenuAction(self, sender, action, idx):
        return self.sessionController.handleAction(sender, idx)
