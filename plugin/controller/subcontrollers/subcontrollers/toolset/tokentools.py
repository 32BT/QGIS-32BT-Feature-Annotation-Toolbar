

from qgis.PyQt.QtWidgets import QMenu

from .actionset import ActionSet
from .actions import MenuActionMarkerAppend
from .actions import ToolActionMarkerAppend
from .actions import ToolActionMarkerModify
from .actions import ToolActionMarkerRemove

from .maptools import PanningMarkerMapTool


################################################################################
### Language
################################################################################

import sys
_MODULE = sys.modules.get(__name__.split('.')[0])
_LABELS = _MODULE.LANGUAGE.LABELS({
        "CTXMENU": { "TITLE": "Markers" }
    })

################################################################################
### Controller
################################################################################

class TokenTools(ActionSet):
    def __init__(self, iface, toolBar):
        super().__init__(
            MenuActionMarkerAppend(),
            ToolActionMarkerAppend(),
            ToolActionMarkerModify(),
            ToolActionMarkerRemove())

        toolBar.addSeparator()
        toolBar.addActions([
            self.getAction(1),
            self.getAction(2),
            self.getAction(3)])

        self._menu = QMenu(_LABELS.CTXMENU.TITLE)
        self._menu.addActions([
            self.getAction(0),
            self.getAction(2),
            self.getAction(3)])

        '''
        The toolbar-version of markerAppend requires a mapTool in order
        to acquire a mapLocation from the user.
        The contextmenu-version of markerAppend gets the mapLocation from the
        contextMenu mouseEvent during the prepareContextMenu signal.
        (See self.prepareContextMenu below.)

        The contextmenu-version can remain connected straight to our signals,
        but the toolbar-version needs to be preprocessed locally to start
        the maptool and acquire the desired mapLocation.
        '''
        self._iface = iface
        self._appendAction = self.getAction(1)
        self._appendAction.handleAction.disconnect(self.handleAction)
        self._appendAction.handleAction.connect(self.handleAppend)

        mapCanvas = self._iface.mapCanvas()
        mapCanvas.contextMenuAboutToShow.connect(self.prepareContextMenu)

    def __del__(self):
        mapCanvas = self._iface.mapCanvas()
        mapCanvas.contextMenuAboutToShow.disconnect(self.prepareContextMenu)

    ########################################################################
    '''
    MarkersController expects a mapLocation to be attached to the actionAppend.
    If the ctxmenu-actionAppend is triggered, then the mouseEvent is used.
    If the toolbar-actionAppend is triggered, then a maptool will be started,
    and the canvasClicked result will be used.
    '''
    def prepareContextMenu(self, menu, mouseEvent):
        appendAction = self.getAction(0)
        appendAction.mapLocation = mouseEvent.originalMapPoint()
        menu.addMenu(self._menu)

    ########################################################################
    '''
    Handle markerAppend action ourself in order to obtain mapLocation.
    Once we have the mapLocation, the action is transmitted.
    '''

    def handleAppend(self, action):
        mapCanvas = self._iface.mapCanvas()
        if action.isChecked():
            self._savedTool = mapCanvas.mapTool()
            mapCanvas.setMapTool(self._markerMapTool(mapCanvas))
        elif hasattr(self, '_savedTool'):
            mapCanvas.setMapTool(self._savedTool)

    def _markerMapTool(self, mapCanvas):
        if not hasattr(self, '_marker'):
            self._marker = PanningMarkerMapTool(mapCanvas)
            self._marker.setAction(self._appendAction)
            self._marker.canvasClicked.connect(self._canvasClicked)
        return self._marker

    def _canvasClicked(self, location=None, button=None):
        self._appendAction.mapLocation = location
        self.emitAction(self._appendAction)
