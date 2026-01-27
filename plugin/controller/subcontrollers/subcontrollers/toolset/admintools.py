

from qgis.PyQt.QtCore import QObject, pyqtSignal

from .actions import ToolActionMarkerFreeze
from .actions import ToolActionMarkerExport
from .actions import ToolActionMarkerArchive


################################################################################
### Controller
################################################################################

class AdminTools(QObject):
    updateAction = pyqtSignal(object)
    handleAction = pyqtSignal(object)

    def __init__(self, iface, toolBar):
        super().__init__()
        self._iface = iface

        self._markerFreeze = ToolActionMarkerFreeze(self)
        self._markerExport = ToolActionMarkerExport(self)
        self._markerArchive = ToolActionMarkerArchive(self)

        action1 = toolBar.addSeparator()
        action2 = toolBar.addAction(self._markerFreeze)
        action3 = toolBar.addAction(self._markerExport)
        action4 = toolBar.addAction(self._markerArchive)
        self._actions = [action1, action2, action3, action4]

    def __del__(self):
        for action in self._actions:
            parent = action.parent()
            parent.removeAction(action)

    ########################################################################

    def updateActions(self):
        self._markerFreeze.update()
        self._markerExport.update()
        self._markerArchive.update()
