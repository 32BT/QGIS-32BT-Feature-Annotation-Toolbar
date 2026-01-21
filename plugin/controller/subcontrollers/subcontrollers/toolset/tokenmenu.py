

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

from .toolset import ToolSet
from ..qgs.mapcanvas import MapCanvas

class TokenMenu(ToolSet):

    def __init__(self, mapCanvas):
        super().__init__(QMenu(_LABELS.MENU_TITLE), {
            _LABELS.MENU_ITEM1: None,
            _LABELS.MENU_ITEM2: None,
            _LABELS.MENU_ITEM3: None})
        self._mapCanvas = MapCanvas(mapCanvas)
        self._mapCanvas.connectMenuHandler(self.prepareContextMenu)

    def __del__(self):
        self._mapCanvas.disconnectMenuHandler(self.prepareContextMenu)
        self._mapCanvas = None

    def prepareContextMenu(self, menu: QMenu, event: QgsMapMouseEvent):
        self.updateActions()
        if len(menu.actions()) == 1:
            menu.addSeparator()
        action = menu.addMenu(self._toolBox)

