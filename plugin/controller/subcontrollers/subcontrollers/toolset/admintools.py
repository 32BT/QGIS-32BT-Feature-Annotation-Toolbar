

from .actionset import ActionSet
from .actions import ToolActionMarkerFreeze
from .actions import ToolActionMarkerExport
from .actions import ToolActionMarkerArchive

################################################################################
### Controller
################################################################################

class AdminTools(ActionSet):
    def __init__(self, iface, toolBar):
        super().__init__(
            ToolActionMarkerFreeze(),
            ToolActionMarkerExport(),
            ToolActionMarkerArchive())

        self._toolBar = toolBar
        self.appendTo(self._toolBar)

    def __del__(self):
        self.removeFrom(self._toolBar)
