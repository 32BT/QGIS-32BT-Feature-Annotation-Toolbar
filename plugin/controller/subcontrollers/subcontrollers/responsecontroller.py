
from qgis.core import *
from qgis.gui import *
from qgis.PyQt.QtCore import *

################################################################################
### Imports
################################################################################

# Action indices
from .actionscontroller import ACTION

# ResponseController handles Sessions and Markers
from .sessioncontroller import SessionController
from .markerscontroller import MarkersController

# ResponseController requires TMS.LAYER functions
from . import tms as TMS
'''
TMS = Token Management System
'''
################################################################################
'''
WARNING!
ResponseController is currently bypassed by TokenController which short-circuits
the connections directly to the Session- and MarkersControllers.
'''
################################################################################

class ResponseController:
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
    ### Validate Action
    ########################################################################

    def updateAction(self, action, idx):
        action.setEnabled(self.validateAction(action, idx))

    def validateAction(self, action, idx):
        if idx == ACTION.INDEX.RESET:
            return self.sessionController.validateAction(action, idx)
        else:
            return self.markersController.validateAction(action, idx)

    ########################################################################
    ### Handle Action
    ########################################################################

    def handleAction(self, sender, idx):
        if idx == ACTION.INDEX.RESET:
            return self.startSession()
        if idx == ACTION.INDEX.APPEND:
            location = sender.lastMapLocation
            return self.startMarker(location)
        if idx == ACTION.INDEX.MODIFY:
            return self.modifyMarker()
        if idx == ACTION.INDEX.REMOVE:
            return self.removeMarker()

    def startSession(self):
        return self.sessionController.startSession()

    def startMarker(self, location):
        return self.markersController.startMarker(location)

    def modifyMarker(self):
        return self.markersController.modifyMarker()

    def removeMarker(self):
        return self.markersController.removeMarker()


