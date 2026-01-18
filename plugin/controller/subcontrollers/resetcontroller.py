

from qgis.PyQt.QtCore import *

from .subcontrollers.toolset import ResetTools

################################################################################
### ResetController
################################################################################
'''
First tool in a toolbar is usually a start button. This button is controlled
separately by the resetcontroller as it is a metaproces. It emits two signals:
1. a signal to request the validity of the currently active layer and selection,
2. a signal if the resetaction was triggered.

This allows another controller to act as delegate for the signals. This usually
is the main controller:

    maincontroller <--------|
     |                      |
     |  ResetController     |
     |      validateReset --|
     |      handleReset   --|
     |
     |->ToolsController


1. ResetController detects changes in layer&selection
2. ResetController signals validateReset
3. MainController asks ToolsController: is layer&selection valid?
4. MainController then enables or disables Reset accordingly

If layer&selection was valid and user subsequently clicks reset:
5. ResetController signals resetClicked
6. MainController restarts ToolsetController

'''
class ResetController(QObject):
    validateReset = pyqtSignal()
    resetClicked = pyqtSignal()

    def __init__(self, iface, toolBar, icon="mActionRunSelected"):
        super().__init__()
        self._iface = iface
        self._tools = ResetTools(toolBar, icon)
        self._tools.resetClicked.connect(self.resetClicked)

    def setDelegate(self, delegate):
        if hasattr(delegate, "validateReset"):
            self.validateReset.connect(delegate.validateReset)
        if hasattr(delegate, "resetClicked"):
            self.resetClicked.connect(delegate.resetClicked)

    def updateActions(self):
        self.validateReset.emit()

    def setEnabled(self, enable=True):
        self._tools.enableActions(enable)


