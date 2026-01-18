

from .toolset import ToolSet


class TokenTools(ToolSet):
    class TOOL:
        class BUTTON1:
            NAME = "Add Marker"
            ICON = "AddMarker"
        class BUTTON2:
            NAME = "Edit Marker"
            ICON = "EditMarker"
        class BUTTON3:
            NAME = "Remove Marker"
            ICON = "RemoveMarker"


    def __init__(self, toolBar):
        super().__init__(toolBar, {
            self.TOOL.BUTTON1.NAME: self.TOOL.BUTTON1.ICON,
            self.TOOL.BUTTON2.NAME: self.TOOL.BUTTON2.ICON,
            self.TOOL.BUTTON3.NAME: self.TOOL.BUTTON3.ICON
        })

        # Add Marker is a MapTool:
        self._actions[0].setCheckable(True)
