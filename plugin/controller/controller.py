

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

from .subcontrollers import ResetController
from .subcontrollers import TokenController
from .selection import Selection

################################################################################
### Controller
################################################################################
'''
Controller is the main controller.
It merely manages two subcontrollers that do the actual work.

Controller
    ResetController <-- responsible for reset button
        ResetTools
    TokenController <-- responsible for token buttons
        ActionsController
            TokenTools
            TokenMenus
        SessionController
        MarkersController
'''
class Controller(QObject):
    _NAME = "Feature Annotation Controller"
    _GUID = _IDENTITY.PREFIX+_NAME.replace(" ", "")

    def __init__(self, iface, toolBar, resetIcon="StartSession"):
        super().__init__()
        self._resetController = ResetController(iface, toolBar, resetIcon)
        self._tokenController = TokenController(iface, toolBar)

        self._resetController.setDelegate(self)
        self._selection = Selection(iface)
        self._selection.changed.connect(self.selectionChanged)
        self.updateActions()

    ########################################################################
    ### Selection response
    ########################################################################

    def selectionChanged(self, layer):
        if hasattr(self._resetController, 'selectionChanged'):
            self._resetController.selectionChanged(layer)
        if hasattr(self._tokenController, 'selectionChanged'):
            self._tokenController.selectionChanged(layer)
        self.updateActions()

    def updateActions(self):
        self._resetController.updateActions()
        self._tokenController.updateActions()

    ########################################################################
    ### ResetController delegation
    ########################################################################

    def validateReset(self):
        self._resetController.setEnabled(True)

    def resetClicked(self):
        self._tokenController.resetClicked()

