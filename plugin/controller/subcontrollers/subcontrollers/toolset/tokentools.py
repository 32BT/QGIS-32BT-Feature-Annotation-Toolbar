

from .toolset import ToolSet

################################################################################
### Language
################################################################################
'''
'''
import sys
_MODULE = sys.modules.get(__name__.split('.')[0])
_LABELS = _MODULE.LANGUAGE.LABELS({
    "TOOLBAR_ITEM1": "Add Marker",
    "TOOLBAR_ITEM2": "Edit Marker",
    "TOOLBAR_ITEM3": "Remove Markers",
    "TOOLBAR_ITEM4": "Lock Markers",
    "TOOLBAR_ITEM5": "Export Markers",
    "TOOLBAR_ITEM6": "Archive Markers"
    })

################################################################################
### TokenTools
################################################################################

class TokenTools(ToolSet):
    class TOOL:
        class BUTTON1:
            NAME = _LABELS.TOOLBAR_ITEM1
            ICON = "marker_create"
        class BUTTON2:
            NAME = _LABELS.TOOLBAR_ITEM2
            ICON = "marker_modify"
        class BUTTON3:
            NAME = _LABELS.TOOLBAR_ITEM3
            ICON = "marker_delete"
        class BUTTON4:
            NAME = _LABELS.TOOLBAR_ITEM4
            ICON = "marker_freeze"
        class BUTTON5:
            NAME = _LABELS.TOOLBAR_ITEM5
            ICON = "marker_export"
        class BUTTON6:
            NAME = _LABELS.TOOLBAR_ITEM6
            ICON = "marker_archive"

    def __init__(self, toolBar):
        super().__init__(toolBar, {
            self.TOOL.BUTTON1.NAME: self.TOOL.BUTTON1.ICON,
            self.TOOL.BUTTON2.NAME: self.TOOL.BUTTON2.ICON,
            self.TOOL.BUTTON3.NAME: self.TOOL.BUTTON3.ICON,
            self.TOOL.BUTTON4.NAME: self.TOOL.BUTTON4.ICON,
            self.TOOL.BUTTON5.NAME: self.TOOL.BUTTON5.ICON,
            self.TOOL.BUTTON6.NAME: self.TOOL.BUTTON6.ICON
        })

        # toolbarActionAppend is a MapTool
        self.action(0).setCheckable(True)
        self.action(0).setObjectName("toolbarActionCreate")
        self.action(1).setObjectName("toolbarActionModify")
        self.action(2).setObjectName("toolbarActionDelete")
        self.action(3).setObjectName("toolbarActionFreeze")
        self.action(4).setObjectName("toolbarActionExport")
        self.action(5).setObjectName("toolbarActionArchive")
        toolBar.insertSeparator(self.action(3))

