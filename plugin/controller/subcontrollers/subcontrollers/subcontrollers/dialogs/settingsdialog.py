

from qgis.core import *
from qgis.PyQt import uic
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtWidgets import *

from .storagesettings import StorageSettings

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
### Storage Dialog
################################################################################
'''
'''

class Dialog(QDialog, _form()):

    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(_LABELS.TITLE)
        self._storageSettings = StorageSettings()
        self.layout().insertWidget(0, self._storageSettings)

        self.adminTools.setText(_LABELS.ADMINTOOLS.LABEL)

    def askSettings(self, params=None):
        params = params or {}
        self._storageSettings.setPath(params.get('path'))
        self.adminTools.setChecked(params.get('show'))
        if self.exec():
            return params

