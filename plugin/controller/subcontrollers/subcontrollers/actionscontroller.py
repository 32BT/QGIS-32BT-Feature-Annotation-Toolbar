

################################################################################
### Imports
################################################################################

# ActionsController uses signals
from qgis.PyQt.QtCore import QObject, pyqtSignal

# ActionsController handles a toolbar and a contextmenu
from .toolset import TokenTools
from .tokenmenu import TokenMenu

# The toolbar contains a maptool
from .qgs.maptools import PanningMarker as PanningMarkerMapTool

################################################################################
### Definitions
################################################################################

class ACTION:
    class INDEX:
        RESET = 0
        APPEND = 1
        MODIFY = 2
        REMOVE = 3

################################################################################
'''
Actions and Response have been split into separate files for clarity.

ActionsController merges toolbar- and menuactions into a single actionsignal.
Reset is a meta-action which is handled by the main controller.

ActionsController emits two signals:

    updateAction.emit(...)
    -- Allows Responder to update actionstates.

    handleAction.emit(sender=self, index=ACTION.INDEX...)
    -- Allows Responder to respond to action
'''

class ActionsController(QObject):
    updateAction = pyqtSignal(object, object)
    handleAction = pyqtSignal(object, object)

    def __init__(self, iface, toolBar):
        super().__init__()

        self._iface = iface

        self._reset = None
        #self._reset = ResetTools(toolBar, icon="StartSession")
        #self._reset.updateAction.connect(self._updateAction)
        #self._reset.action(0).triggered.connect(self._parseReset)

        self._tools = TokenTools(toolBar)
        self._tools.updateAction.connect(self._updateAction)
        self._tools.action(0).triggered.connect(self._parseToolAction1)
        self._tools.action(1).triggered.connect(self._parseToolAction2)
        self._tools.action(2).triggered.connect(self._parseToolAction3)

        self._menus = TokenMenu(iface.mapCanvas())
        self._menus.updateAction.connect(self._updateAction)
        self._menus.action(0).triggered.connect(self._parseMenuAction1)
        self._menus.action(1).triggered.connect(self._parseMenuAction2)
        self._menus.action(2).triggered.connect(self._parseMenuAction3)

        self.lastMapLocation = None


    def setResponder(self, controller):
        self.updateAction.connect(controller.updateAction)
        self.handleAction.connect(controller.handleAction)

    ########################################################################
    ### Update Actions
    ########################################################################

    # Validate toolbar actions (called by maincontroller)
    def updateActions(self):
        if self._reset: self._reset.updateActions()
        if self._tools: self._tools.updateActions()

    # Translate sender.action to ACTION.INDEX
    def _updateAction(self, sender, action):
        idx = sender.actions().index(action)
        idx += sender != self._reset
        self.updateAction.emit(action, idx)

    ########################################################################
    ### Handle Actions
    ########################################################################
    '''
    Not implemented because this controller uses direct connections
    '''
    def _handleAction(self, sender, action):
        raise NotImplementedError

    ########################################################################
    ### ToolAction Handlers
    ########################################################################
    '''
    Action 1 is different depending on toolbutton vs menuitem:
    - toolAction0 starts a MapTool to acquire a mappoint from the user.
    - menuAction0 fetches the mapPoint from the contextmenu event.

    Actions 2&3 are equivalent for both.
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

    def _parseToolAction2(self):
        self._parseMenuAction2()

    def _parseToolAction3(self):
        self._parseMenuAction3()

    ########################################################################
    ### MenuAction Handlers
    ########################################################################

    def _parseMenuAction1(self):
        self.canvasClicked(self._menus.lastMapLocation())

    def _parseMenuAction2(self):
        self.emitAction(ACTION.INDEX.MODIFY)

    def _parseMenuAction3(self):
        self.emitAction(ACTION.INDEX.REMOVE)

    ########################################################################
    ### Response
    ########################################################################

    def canvasClicked(self, location):
        self.lastMapLocation = location
        self.emitAction(ACTION.INDEX.APPEND)

    def emitAction(self, idx):
        self.handleAction.emit(self, idx)

