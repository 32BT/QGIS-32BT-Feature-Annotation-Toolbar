

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
    "CTXMENU": {
        "TITLE": "Annotation Markers",
        "ITEM1": "Add Marker...",
        "ITEM2": "Edit Marker...",
        "ITEM3": "Remove Marker..."
    }
})

################################################################################
### ContextMenu
################################################################################

from .toolset import ToolSet

class TokenMenu(ToolSet):

    def __init__(self, mapCanvas):
        super().__init__(QMenu(_LABELS.CTXMENU.TITLE), {
            _LABELS.CTXMENU.ITEM1: None,
            _LABELS.CTXMENU.ITEM2: None,
            _LABELS.CTXMENU.ITEM3: None})
        # In this case we also own the toolBox
        self._toolBox.setObjectName("fat:contextMenu")
        self.action(0).setObjectName("fat:ctxmenuActionAppend")
        self.action(1).setObjectName("fat:ctxmenuActionModify")
        self.action(2).setObjectName("fat:ctxmenuActionRemove")
        # Connect to mapCanvas
        self._mapCanvas = mapCanvas
        self._mapCanvas.contextMenuAboutToShow.connect(self.prepareContextMenu)

    def __del__(self):
        self._mapCanvas.contextMenuAboutToShow.disconnect(self.prepareContextMenu)
        self._mapCanvas = None


    def prepareContextMenu(self, menu, qgsmouseEvent):
        self.updateActions()
        if len(menu.actions()) == 1:
            menu.addSeparator()
        action = menu.addMenu(self._toolBox)

