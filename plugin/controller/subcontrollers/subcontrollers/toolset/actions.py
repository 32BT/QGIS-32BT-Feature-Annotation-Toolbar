

from qgis.core import *
from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtGui import QAction

from .maptools import PanningMarkerMapTool

################################################################################
### Definitions
################################################################################
'''
'''
class ACTION:
    class INDEX:
        APPEND = 1
        MODIFY = 2
        REMOVE = 3
        FREEZE = 4
        EXPORT = 5
        ARCHIVE = 6

################################################################################
### Language
################################################################################
'''
'''
import sys
_MODULE = sys.modules.get(__name__.split('.')[0])
_LABELS = _MODULE.LANGUAGE.LABELS({
        "ACTION": {
            "APPEND": "Add Marker...",
            "MODIFY": "Edit Marker...",
            "REMOVE": "Remove Marker...",
            "FREEZE": "Lock Markers...",
            "EXPORT": "Export Markers...",
            "ARCHIVE": "Archive Markers..." }
    })

################################################################################
### BaseAction
################################################################################

from .icons import loadIcon

class Action(QAction):
    updateAction = pyqtSignal(object)
    handleAction = pyqtSignal(object)

    def __init__(self, responder=None):
        super().__init__(loadIcon(self._ICON), self._TEXT)
        self.setObjectName(self._UIID)
        self.triggered.connect(self._triggered)
        if responder:
            self.updateAction.connect(responder.updateAction)
            self.handleAction.connect(responder.handleAction)

    def update(self):
        self.updateAction.emit(self)

    def _triggered(self):
        self.handleAction.emit(self)

################################################################################
'''
MenuActionMarkerAppend is the contextmenu-version. It does not require
additional user-input for a maplocation.
'''
class MenuActionMarkerAppend(Action):
    INDEX = ACTION.INDEX.APPEND
    _ICON = "marker_append"
    _TEXT = _LABELS.ACTION.APPEND
    _UIID = "fat:ctxmenu:actionAppend"

################################################################################
'''
ToolActionMarkerAppend is the toolbar-version. It requires additional input
using a MapTool to acquire a maplocation.
'''
class ToolActionMarkerAppend(MenuActionMarkerAppend):
    _UIID = "fat:toolbar:actionAppend"

    def __init__(self, responder):
        super().__init__(responder)
        self.setCheckable(True)

################################################################################

class ToolActionMarkerModify(Action):
    INDEX = ACTION.INDEX.MODIFY
    _ICON = "marker_modify"
    _TEXT = _LABELS.ACTION.MODIFY
    _UIID = "fat:toolbar:actionModify"

################################################################################

class ToolActionMarkerRemove(Action):
    INDEX = ACTION.INDEX.REMOVE
    _ICON = "marker_remove"
    _TEXT = _LABELS.ACTION.REMOVE
    _UIID = "fat:toolbar:actionRemove"

################################################################################

class ToolActionMarkerFreeze(Action):
    INDEX = ACTION.INDEX.FREEZE
    _ICON = "marker_freeze"
    _TEXT = _LABELS.ACTION.FREEZE
    _UIID = "fat:toolbar:actionFreeze"

################################################################################

class ToolActionMarkerExport(Action):
    INDEX = ACTION.INDEX.EXPORT
    _ICON = "marker_export"
    _TEXT = _LABELS.ACTION.EXPORT
    _UIID = "fat:toolbar:actionExport"

################################################################################

class ToolActionMarkerArchive(Action):
    INDEX = ACTION.INDEX.ARCHIVE
    _ICON = "marker_archive"
    _TEXT = _LABELS.ACTION.ARCHIVE
    _UIID = "fat:toolbar:actionArchive"

################################################################################
