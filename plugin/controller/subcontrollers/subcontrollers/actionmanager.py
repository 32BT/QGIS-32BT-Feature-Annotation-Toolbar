

################################################################################
### Imports
################################################################################

# ActionsController uses signals
from qgis.PyQt.QtCore import QObject, pyqtSignal

# ActionsController handles a toolbar and a contextmenu
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
        APPEND = 1
        MODIFY = 2
        REMOVE = 3
        ARCHIVE = 4

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

    '''
    Both Toolbar as well as Contextmenu actions trigger updates.
    These are transferred to the responder (ActionHandler)
    '''
    # Translate sender.action to ACTION.INDEX
    def _updateAction(self, sender, action, idx):
        self.updateAction.emit(action, idx+1)

    ########################################################################
    ### Handle Actions
    ########################################################################
    '''
    Transfer all actions to responder, except toolbarAction1 which first
    needs to run a MapTool.
    '''
    def _handleAction(self, sender, action, idx):
        #raise NotImplementedError
        if action != self._tools.action(0):
            self.handleAction.emit(self, idx+1)
        else:
            self._parseToolAction1(action.isChecked())

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
        self.handleAction.emit(self, ACTION.INDEX.APPEND)



