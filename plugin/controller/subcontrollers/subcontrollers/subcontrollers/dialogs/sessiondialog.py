

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
Pattern:

    note = NoteDialog(parent).askInfo(layer, marker)
    if note:
        marker = marker or Marker()
        marker.date = date
        marker.note = note
'''

class Dialog(QDialog, _form()):
    _LABEL = _LABELS.SESSIONDIALOG_LABEL

    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(_LABELS.SESSIONDIALOG_TITLE)
        self.mainLabel.setText(_LABELS.SESSIONDIALOG_LABEL)
        self.comboBoxLabel.setText(_LABELS.SESSIONDIALOG_NAMELABEL)

    # Ask user for existing or new session name
    # pattern: SessionDialog(parent).askSessionName(sessionSet)
    def askSessionName(self, sessionSet):
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
        return self.comboBox.currentText()
