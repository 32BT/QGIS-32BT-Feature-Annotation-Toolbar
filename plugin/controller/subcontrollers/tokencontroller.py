

################################################################################
###
################################################################################

from .subcontrollers import ActionsController
from .subcontrollers import SessionController
from .subcontrollers import MarkersController

class TokenController:
    def __init__(self, iface, toolBar):
        self._iface = iface
        self._actionsController = ActionsController(iface, toolBar)
        self._markersController = MarkersController(iface)
        self._actionsController.setResponder(self._markersController)

    def updateActions(self):
        self._actionsController.updateActions()

    def resetClicked(self):
        if not hasattr(self, '_sessionController'):
            self._sessionController = SessionController(self._iface)
        self._sessionController.startSession()
