
from qgis.PyQt.QtGui import QAction
from qgis.PyQt.QtCore import QObject, pyqtSignal

################################################################################
### BaseAction
################################################################################
'''
Action is a QAction that will send "self" when triggered. It also adds an
equivalent update signal. It thereby conforms to the ActionLink protocol,
which allows it to link to a chain of command.
'''

from .icons import loadIcon

class Action(QAction):
    updateAction = pyqtSignal(object)
    handleAction = pyqtSignal(object)

    def __init__(self, responder=None):
        super().__init__(loadIcon(self._ICON), self._TEXT)
        self.setObjectName(self._UIID)
        self.triggered.connect(self._triggered)
        if responder: self.setResponder(responder)

    def update(self):
        self.updateAction.emit(self)

    def _triggered(self):
        self.handleAction.emit(self)

    def setResponder(self, responder):
        self.updateAction.connect(responder.updateAction)
        self.handleAction.connect(responder.handleAction)

################################################################################
### ActionLink
################################################################################
'''
ActionLink object allows a derived object to be part of an actionchain.

e.g.:
    ActionManager(ActionLink) -----> responder: ActionHandler
        TokenTools(ActionLink)
            actionMarkerAppend(Action)
            ...

    The actionMarkerAppend trigger will move up the chain to ActionManager
    which in turn will send the signal to its responder: ActionHandler
'''

class ActionLink(QObject):
    updateAction = pyqtSignal(object)
    handleAction = pyqtSignal(object)

    def emitUpdate(self, action):
        self.updateAction.emit(action)

    def emitAction(self, action):
        self.handleAction.emit(action)

    def setResponder(self, responder):
        self.updateAction.connect(responder.updateAction)
        self.handleAction.connect(responder.handleAction)

################################################################################
