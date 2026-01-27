

from qgis.PyQt.QtCore import QObject, pyqtSignal
from qgis.PyQt.QtWidgets import QMenu


from .actions import MenuActionMarkerAppend
from .actions import ToolActionMarkerAppend
from .actions import ToolActionMarkerModify
from .actions import ToolActionMarkerRemove

from .maptools import PanningMarkerMapTool


################################################################################
### Language
################################################################################
'''
'''
import sys
_MODULE = sys.modules.get(__name__.split('.')[0])
_LABELS = _MODULE.LANGUAGE.LABELS({
        "CTXMENU": { "TITLE": "Markers" }
    })

################################################################################
### Controller
################################################################################

class TokenTools(QObject):
    updateAction = pyqtSignal(object)
    handleAction = pyqtSignal(object)

    def __init__(self, iface, toolBar):
        super().__init__()
        self._iface = iface

        '''
        The toolbar-version of markerAppend requires maptoolinteraction.
        The contextmenu-version of markerAppend does not.
        (It gets the mapLocation from the contextMenu mouseEvent during the
        prepareContextMenu signal. See self.prepareContextMenu below).
        '''
        self._markerAppend_menu = MenuActionMarkerAppend(self)
        self._markerAppend = ToolActionMarkerAppend(self)
        self._markerModify = ToolActionMarkerModify(self)
        self._markerRemove = ToolActionMarkerRemove(self)

        # Need to handle toolbar-version of markerAppend locally
        self._markerAppend.handleAction.disconnect(self.handleAction)
        self._markerAppend.handleAction.connect(self.handleAppend)

        # Add actions to toolBar
        if toolBar.actions(): toolBar.addSeparator()
        toolBar.addAction(self._markerAppend)
        toolBar.addAction(self._markerModify)
        toolBar.addAction(self._markerRemove)

        # Also create submenu for contextmenu
        ctxMenu = QMenu(_LABELS.CTXMENU.TITLE)
        ctxMenu.addAction(self._markerAppend_menu)
        ctxMenu.addAction(self._markerModify)
        ctxMenu.addAction(self._markerRemove)
        self._ctxMenu = ctxMenu

        mapCanvas = self._iface.mapCanvas()
        mapCanvas.contextMenuAboutToShow.connect(self.prepareContextMenu)

    def __del__(self):
        mapCanvas = self._iface.mapCanvas()
        mapCanvas.contextMenuAboutToShow.disconnect(self.prepareContextMenu)

    ########################################################################

    def updateActions(self):
        self._markerAppend.update()
        self._markerModify.update()
        self._markerRemove.update()

    ########################################################################
    '''
    MarkersController expects a mapLocation to be attached to the actionAppend.
    If the ctxmenu-actionAppend is triggered, then the mouseEvent is used.
    If the toolbar-actionAppend is triggered, then a maptool will be started,
    and the canvasClicked result will be used.
    '''
    def prepareContextMenu(self, menu, mouseEvent):
        self._markerAppend_menu.mapLocation = mouseEvent.originalMapPoint()
        self._markerAppend_menu.update()
        menu.addMenu(self._ctxMenu)

    ########################################################################
    '''
    Handle markerAppend action ourself in order to obtain mapLocation.
    Once we have the mapLocation, the action is tranferred to markersController.
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
            self._marker.setAction(self._markerAppend)
            self._marker.canvasClicked.connect(self._canvasClicked)
        return self._marker

    def _canvasClicked(self, location=None, button=None):
        self._markerAppend.mapLocation = location
        self.handleAction.emit(self._markerAppend)
