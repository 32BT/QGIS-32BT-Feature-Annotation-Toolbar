

################################################################################
###
################################################################################

from .subcontrollers import ActionManager
from .subcontrollers import ActionHandler


class ToolController:
    def __init__(self, iface, toolBar):
        self._iface = iface
        self._actionManager = ActionManager(iface, toolBar)
        self._actionHandler = ActionHandler(iface)
        self._actionManager.setResponder(self._actionHandler)

    ########################################################################
    ### Action Updates
    ########################################################################

    # self
    def updateActions(self):
        self._actionManager.updateActions()

    # Delegate
    def updateMenuAction(self, sender, action, idx):
        self._actionHandler.updateMenuAction(sender, action, idx)

    def handleMenuAction(self, sender, action, idx):
        self._actionHandler.handleMenuAction(sender, action, idx)
