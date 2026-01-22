

from qgis.core import *
from qgis.PyQt import uic
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtWidgets import *


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
    "SESSIONDIALOG_TITLE":
        "Start Session",
    "SESSIONDIALOG_LABEL": [
        "Select an existing session, or enter a new sessionname.",
        "(Database is: '{}')"],
    "SESSIONDIALOG_NAMELABEL":
        "Session:"
    })

_LABELS.SESSIONDIALOG_LABEL = '\n'.join(_LABELS.SESSIONDIALOG_LABEL)

################################################################################
### Session Dialog
################################################################################
'''
Ask user for existing or new session name
pattern:
    result = SessionDialog(parent).askInput(sessionSet)
'''

class Dialog(QDialog, _form()):
    _LABEL = _LABELS.SESSIONDIALOG_LABEL

    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(_LABELS.SESSIONDIALOG_TITLE)
        self.mainLabel.setText(_LABELS.SESSIONDIALOG_LABEL)
        self.comboBoxLabel.setText(_LABELS.SESSIONDIALOG_NAMELABEL)

    def askInput(self, sessionSet):
        if sessionSet: self.setSessionSet(sessionSet)
        if self.exec():
            return self.textValue()

    def setSessionSet(self, sessionSet):
        db = sessionSet.parent()
        self.setWindowTitle(db.name())
        self.mainLabel.setText(self._LABEL.format(db.path()))
        self.comboBox.clear()
        self.comboBox.addItems(list(sessionSet.folderItemNames()))
        self.comboBox.setEditText(sessionSet.generateItemName())

    def textValue(self):
        return self.comboBox.currentText().strip()
