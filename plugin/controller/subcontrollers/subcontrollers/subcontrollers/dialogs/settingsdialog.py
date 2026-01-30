

from qgis.core import *
from qgis.PyQt import uic
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtWidgets import *

from .storagesettings import StorageSettings
from ..database import Database

################################################################################

import os

def _form():
    path, ext = os.path.splitext(__file__)
    form, _ = uic.loadUiType(path+'.ui')
    return form

################################################################################
### Labels
################################################################################

import sys
_MODULE = sys.modules.get(__name__.split('.')[0])
_LABELS = _MODULE.LANGUAGE.LABELS({
    "SETTINGSDIALOG": {
        "TITLE":
            "Settings",
        "ADMINTOOLS": {
            "LABEL":
                "Show Admin Tools"
            }
        }
    })

_LABELS = _LABELS.SETTINGSDIALOG

################################################################################
### Settings Dialog
################################################################################
'''
'''

class Dialog(QDialog, _form()):
    settingsChanged = pyqtSignal(object)

    class OPTIONS:
        class ADMINTOOLS:
            SHOW = "options/admintools/show"

    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(_LABELS.TITLE)
        self._storageSettings = StorageSettings()
        self.layout().insertWidget(0, self._storageSettings)
        self.adminTools.setText(_LABELS.ADMINTOOLS.LABEL)
        self.adminTools.toggled.connect(self.adminToolsToggled)

    def adminToolsToggled(self, isChecked):
        path = self._storageSettings.getPath()
        show = self.adminTools.isChecked()
        result = dict(path=path, show=show)
        self.settingsChanged.emit(result)

    def askSettings(self, responder=None):
        self.loadDialogSettings()
        if hasattr(responder, 'settingsChanged'):
            self.settingsChanged.connect(responder.settingsChanged)
        if self.exec():
            return self.saveDialogSettings()
        self.loadDialogSettings()

    def loadDialogSettings(self):
        Settings = _MODULE.plugin.Settings
        path = Database.getGlobalPath()
        show = Settings.getGlobalValue(self.OPTIONS.ADMINTOOLS.SHOW)
        show = show in (True, 'true', 'True', 'TRUE')
        self._storageSettings.setPath(path)
        self.adminTools.setChecked(show)

    def saveDialogSettings(self):
        path = self._storageSettings.getPath()
        show = self.adminTools.isChecked()
        Settings = _MODULE.plugin.Settings
        Database.setGlobalPath(path)
        Settings.setGlobalValue(self.OPTIONS.ADMINTOOLS.SHOW, show)
        return dict(path=path, show=show)
