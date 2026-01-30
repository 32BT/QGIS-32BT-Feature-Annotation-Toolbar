

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

    def show(self, show=True):
        hide = show not in (True, 'true', 'True', 'TRUE')
        self.hide(hide)

    def hide(self, hide=True):
        if hide in (True, 'true', 'True', 'TRUE'):
            self.removeFrom(self._toolBar)
        else:
            self.appendTo(self._toolBar)
