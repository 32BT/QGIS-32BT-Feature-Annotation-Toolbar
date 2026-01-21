

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
    "TOOLBAR_ITEM3": "Remove Marker"})

################################################################################
### TokenTools
################################################################################

class TokenTools(ToolSet):
    class TOOL:
        class BUTTON1:
            NAME = _LABELS.TOOLBAR_ITEM1
            ICON = "marker_append"
        class BUTTON2:
            NAME = _LABELS.TOOLBAR_ITEM2
            ICON = "marker_modify"
        class BUTTON3:
            NAME = _LABELS.TOOLBAR_ITEM3
            ICON = "marker_remove"


    def __init__(self, toolBar):
        super().__init__(toolBar, {
            self.TOOL.BUTTON1.NAME: self.TOOL.BUTTON1.ICON,
            self.TOOL.BUTTON2.NAME: self.TOOL.BUTTON2.ICON,
            self.TOOL.BUTTON3.NAME: self.TOOL.BUTTON3.ICON
        })

        # toolbarActionAppend is a MapTool
        self.action(0).setCheckable(True)
        self.action(0).setObjectName("toolbarActionAppend")
        self.action(1).setObjectName("toolbarActionModify")
        self.action(2).setObjectName("toolbarActionRemove")
