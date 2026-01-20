

import sys
_MODULE = sys.modules.get(__name__.split('.')[0])
_IDENTITY = _MODULE.IDENTITY
_LANGUAGE = _MODULE.LANGUAGE
_LABELS = _LANGUAGE.LABELS()


################################################################################
### Toolbar
################################################################################

class ToolBar:
    _NAME = "Feature Annotation Toolbar"
    _GUID = _IDENTITY.PREFIX+_NAME.replace(" ", "")

    def __new__(cls, iface):
        toolBar = iface.addToolBar(_LABELS(cls._NAME))
        toolBar.setObjectName(cls._GUID)
        return toolBar

################################################################################

from qgis.PyQt.QtCore import *

from .subcontrollers import MenuController
from .subcontrollers import ToolController
from .selection import Selection

################################################################################
### Controller
################################################################################
'''
Controller is the main controller.
It merely manages two subcontrollers that do the actual work.

Controller
    MenuController <-- responsible for session button
    ToolController <-- responsible for marker buttons
        ActionManager
            tokenToolActions
            tokenMenuActions
        ActionHandler
            SessionController
            MarkersController
'''
class Controller(QObject):
    _NAME = "Feature Annotation Controller"
    _GUID = _IDENTITY.PREFIX+_NAME.replace(" ", "")

    def __init__(self, iface, toolBar, menuIcon="menuButton"):
        super().__init__()
        self._menuController = MenuController(iface, toolBar, menuIcon)
        self._toolController = ToolController(iface, toolBar)
        self._menuController.setDelegate(self._toolController)

        self._selection = Selection(iface)
        self._selection.changed.connect(self.selectionChanged)
        self.updateActions()

    ########################################################################
    ### Selection Changed
    ########################################################################

    def selectionChanged(self, layer):
        self.updateActions()

    def updateActions(self):
        self._menuController.updateActions()
        self._toolController.updateActions()

