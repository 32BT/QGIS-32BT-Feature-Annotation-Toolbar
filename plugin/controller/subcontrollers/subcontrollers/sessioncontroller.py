
from .actionscontroller import ACTION

class SessionController:
    def __init__(self, iface):
        self._iface = iface

    def validateAction(self, action, idx):
        return idx == ACTION.INDEX.RESET

    def handleAction(self, sender, idx):
        if idx == ACTION.INDEX.RESET:
            return self.startSession()

    def startSession(self):
        print('SessionController.startSession')
