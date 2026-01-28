

################################################################################
### Imports
################################################################################

# ActionsController uses signals
from qgis.PyQt.QtCore import QObject, pyqtSignal

# ActionsController handles tokentools and admintools
from .toolset.action import ActionLink
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

ActionManager is an ActionLink and emits two signals:

    updateAction(action)
    -- Allows Responder to update actionstates.

    handleAction(action)
    -- Allows Responder to respond to action
'''

class ActionManager(ActionLink):

    def __init__(self, iface, toolBar):
        super().__init__()
        self._tokenTools = TokenTools(iface, toolBar)
        self._tokenTools.setResponder(self)
        self._adminTools = AdminTools(iface, toolBar)
        self._adminTools.setResponder(self)

    def updateActions(self):
        if self._tokenTools: self._tokenTools.updateActions()
        if self._adminTools: self._adminTools.updateActions()



