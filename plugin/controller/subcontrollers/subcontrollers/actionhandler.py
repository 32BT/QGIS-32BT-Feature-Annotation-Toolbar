

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

class ActionHandler(QObject):
    settingsChanged = pyqtSignal(object)

    def __init__(self, iface):
        super().__init__()
        self._iface = iface
        self._sessionController = SessionController(self._iface)
        self._markersController = MarkersController(self._iface)
        self._sessionController.settingsChanged.connect(self.settingsChanged)

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
    def updateAction(self, action):
        return self._markersController.updateAction(action)

    def handleAction(self, action):
        return self._markersController.handleAction(action)

