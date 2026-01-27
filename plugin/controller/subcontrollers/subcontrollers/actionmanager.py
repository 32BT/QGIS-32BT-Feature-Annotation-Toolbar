

################################################################################
### Imports
################################################################################

# ActionsController uses signals
from qgis.PyQt.QtCore import QObject, pyqtSignal

# ActionsController handles tokentools and admintools
from .toolset.tokentools import TokenTools
from .toolset.admintools import AdminTools

################################################################################
### Controller
################################################################################
'''
Actions and Response have been split into separate files for clarity:
    ActionManager creates the actions
    ActionHandler responds to actions

ToolController fuses them together.

The sessionmenu is handled separately. Its actions are channeled through
ToolController directly to ActionHandler.

ActionManager emits two signals:

    updateAction.emit(...)
    -- Allows Responder to update actionstates.

    handleAction.emit(sender=self, index=ACTION.INDEX...)
    -- Allows Responder to respond to action
'''

class ActionManager(QObject):
    updateAction = pyqtSignal(object)
    handleAction = pyqtSignal(object)

    def __init__(self, iface, toolBar):
        super().__init__()
        self._iface = iface

        self._tokenTools = TokenTools(iface, toolBar)
        self._tokenTools.updateAction.connect(self.updateAction)
        self._tokenTools.handleAction.connect(self.handleAction)

        self._adminTools = AdminTools(iface, toolBar)
        self._adminTools.updateAction.connect(self.updateAction)
        self._adminTools.handleAction.connect(self.handleAction)


    # ToolController will set ActionHandler as responder
    def setResponder(self, responder):
        self.updateAction.connect(responder.updateAction)
        self.handleAction.connect(responder.handleAction)


    def updateActions(self):
        if self._tokenTools: self._tokenTools.updateActions()
        if self._adminTools: self._adminTools.updateActions()



