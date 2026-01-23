

from .toolset import ToolSet

################################################################################
### Language
################################################################################
'''
'''
import sys
_MODULE = sys.modules.get(__name__.split('.')[0])
_LABELS = _MODULE.LANGUAGE.LABELS({
    "ADMINTOOLS": {
        "ITEM1": "Lock Markers",
        "ITEM2": "Export Markers",
        "ITEM3": "Archive Markers" }
    })

################################################################################
### TokenTools
################################################################################

class AdminTools(ToolSet):
    class TOOL:
        class BUTTON1:
            NAME = _LABELS.ADMINTOOLS.ITEM1
            ICON = "marker_freeze"
            UIID = "toolbarActionFreeze"
        class BUTTON2:
            NAME = _LABELS.ADMINTOOLS.ITEM2
            ICON = "marker_export"
            UIID = "toolbarActionExport"
        class BUTTON3:
            NAME = _LABELS.ADMINTOOLS.ITEM3
            ICON = "marker_archive"
            UIID = "toolbarActionArchive"

    def __init__(self, toolBar):
        super().__init__(toolBar, {
            self.TOOL.BUTTON1.NAME: self.TOOL.BUTTON1.ICON,
            self.TOOL.BUTTON2.NAME: self.TOOL.BUTTON2.ICON,
            self.TOOL.BUTTON3.NAME: self.TOOL.BUTTON3.ICON
        })

        self.action(0).setObjectName("toolbarActionFreeze")
        self.action(1).setObjectName("toolbarActionExport")
        self.action(2).setObjectName("toolbarActionArchive")

