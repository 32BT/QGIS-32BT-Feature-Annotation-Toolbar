

################################################################################
### Imports
################################################################################

# ActionsController uses signals
from qgis.PyQt.QtCore import QObject, pyqtSignal

# ActionsController handles a toolbar and a contextmenu
from .toolset import AdminTools
from .toolset import TokenTools
from .toolset import TokenMenu

# The toolbar contains a maptool
from .toolset.maptools import PanningMarkerMapTool

################################################################################
### Definitions
################################################################################
'''
ActionManager merges toolbar- and menuactions into a single actionsignal.
The signal emits an ACTION.INDEX.
'''
class ACTION:
    class INDEX:
        CREATE = 1
        MODIFY = 2
        DELETE = 3
        FREEZE = 4
        EXPORT = 5
        ARCHIVE = 6

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
    updateAction = pyqtSignal(object, object)
    handleAction = pyqtSignal(object, object)

    def __init__(self, iface, toolBar):
        super().__init__()
        self._iface = iface

        # Toolbar buttons
        self._tools = TokenTools(toolBar)
        self._tools.updateAction.connect(self._updateAction)
        self._tools.handleAction.connect(self._handleAction)

        # Context menu
        self._menus = TokenMenu(iface.mapCanvas())
        self._menus.updateAction.connect(self._updateAction)
        self._menus.handleAction.connect(self._handleAction)

        self._adminTools = AdminTools(toolBar)
        self._adminTools.updateAction.connect(self._updateAction)
        self._adminTools.handleAction.connect(self._handleAction)

    def setResponder(self, controller):
        self.updateAction.connect(controller.updateAction)
        self.handleAction.connect(controller.handleAction)

    ########################################################################
    ### Update Actions
    ########################################################################
    '''
    Validate toolbar actions, called via maincontroller Selectionchanges.
    (menu actions are validated on-demand)
    '''
    def updateActions(self):
        self._tools.updateActions()
        self._adminTools.updateActions()

    '''
    Both Toolbar as well as Contextmenu actions trigger updates.
    These are transferred to the responder (ActionHandler)
    '''
    # Translate sender.action to ACTION.INDEX
    def _updateAction(self, sender, action, idx):
        if sender == self._tools:
            self.updateAction.emit(action, ACTION.INDEX.CREATE+idx)
        elif sender == self._adminTools:
            self.updateAction.emit(action, ACTION.INDEX.FREEZE+idx)

    ########################################################################
    ### Handle Actions
    ########################################################################
    '''
    Transfer all actions to responder, except toolbarAction1 which first
    needs to run a MapTool.
    '''
    def _handleAction(self, sender, action, idx):
        if sender == self._tools:
            if action == self._tools.action(0):
                return self._parseToolAction1(action.isChecked())
            self.handleAction.emit(self, ACTION.INDEX.CREATE+idx)
        elif sender == self._adminTools:
            self.handleAction.emit(self, ACTION.INDEX.FREEZE+idx)

    ########################################################################
    ### ToolAction Handlers
    ########################################################################
    '''
    Action 1 is different depending on toolbutton vs menuitem:
    - toolAction0 starts a MapTool to acquire a mappoint from the user.
    - menuAction0 fetches the mapPoint from the contextmenu event.
    '''
    def _parseToolAction1(self, isChecked):
        canvas = self._iface.mapCanvas()
        if isChecked:
            self._savedTool = canvas.mapTool()
            canvas.setMapTool(self.markerMapTool())
        elif hasattr(self, '_savedTool'):
            canvas.setMapTool(self._savedTool)

    def markerMapTool(self):
        if not hasattr(self, '_marker'):
            self._marker = PanningMarkerMapTool(self._iface.mapCanvas())
            self._marker.setAction(self._tools.action(0))
            self._marker.canvasClicked.connect(self.canvasClicked)
        return self._marker

    def canvasClicked(self, location=None, button=None):
        #self.lastMapLocation = location
        self.handleAction.emit(self, ACTION.INDEX.CREATE)



