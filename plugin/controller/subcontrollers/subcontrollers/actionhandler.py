
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
        self._sessionController = SessionController(self._iface)
        self._markersController = MarkersController(self._iface)

    ########################################################################
    ### Handle Menu Actions (sessionmenu)
    ########################################################################
    '''
    Receives MENU.ITEM.INDEX types
    '''
    def updateMenuAction(self, sender, action, idx):
        return self._sessionController.updateAction(action, idx)

    def handleMenuAction(self, sender, action, idx):
        return self._sessionController.handleAction(sender, idx)

    ########################################################################
    ### Handle Tool Actions (toolbar and contextmenu)
    ########################################################################
    '''
    Receives ACTION.INDEX types
    '''
    def updateAction(self, action, idx):
        return self._markersController.updateAction(action, idx)

    def handleAction(self, sender, idx):
        return self._markersController.handleAction(sender, idx)

