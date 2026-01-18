
from qgis.PyQt.QtCore import *

from .toolset import ToolSet

'''
The default reseticon is the RunSelected icon as that most likely resembles
the expected logic, even if a custom icon is not available. The RunSelected
icon also has a QGIS counterpart as fallback.

The custom icon is set in de main controller when creating the ResetController.
'''

class ResetTools(ToolSet):
    resetClicked = pyqtSignal()

    def __init__(self, toolBar, iconName="RunSelected"):
        super().__init__(toolBar, {"Start Session": iconName })

    def parseAction(self, action):
        self.resetClicked.emit()
        #super().parseAction(action)
