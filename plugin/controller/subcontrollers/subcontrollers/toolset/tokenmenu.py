

from qgis.gui import *
from qgis.core import *
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtWidgets import *
from qgis.PyQt.QtGui import *

################################################################################
### Language
################################################################################
'''
'''
import sys
_MODULE = sys.modules.get(__name__.split('.')[0])
_LABELS = _MODULE.LANGUAGE.LABELS({
    "MENU_TITLE": "Annotation Markers",
    "MENU_ITEM1": "Add Marker...",
    "MENU_ITEM2": "Edit Marker...",
    "MENU_ITEM3": "Remove Marker..."})

################################################################################
### ContextMenu
################################################################################

from ..qgs.mapcanvas import MapCanvas as MapCanvasController

class TokenMenu(QObject):
    updateAction = pyqtSignal(object, object)
    handleAction = pyqtSignal(object, object)

    def __init__(self, mapCanvas):
        super().__init__()
        self._mapCanvas = MapCanvasController(mapCanvas)
        self._mapCanvas.connectMenuHandler(self.prepareContextMenu)
        self._menu = self.startMenu()

    def __del__(self):
        self._mapCanvas.disconnectMenuHandler(self.prepareContextMenu)
        self._mapCanvas = None


    def startMenu(self):
        menu = QMenu(_LABELS.MENU_TITLE)
        menu.addAction(_LABELS.MENU_ITEM1)
        menu.addAction(_LABELS.MENU_ITEM2)
        menu.addAction(_LABELS.MENU_ITEM3)
        menu.triggered.connect(self.parseMenuAction)
        return menu


    def prepareContextMenu(self, menu: QMenu, event: QgsMapMouseEvent):
        for action in self.actions():
            self.updateAction.emit(self, action)
        if len(menu.actions()) == 1:
            menu.addSeparator()
        action = menu.addMenu(self._menu)

    def parseMenuAction(self, action):
        if action in self._menu.actions():
            self.handleAction.emit(self, action)

    def actions(self):
        return self._menu.actions()

    def action(self, idx):
        try: return self._menu.actions()[idx]
        except IndexError: pass

    def indexOfAction(self, action):
        return self._menu.actions().index(action)

    def lastMapLocation(self):
        eventLoc = self._mapCanvas.getLastEventPosition()
        mapPoint = self._mapCanvas.getMapPointForEventPosition(eventLoc)
        return mapPoint

