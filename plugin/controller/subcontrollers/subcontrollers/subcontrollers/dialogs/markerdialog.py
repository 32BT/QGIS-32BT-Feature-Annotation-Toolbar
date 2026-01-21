

from qgis.core import *
from qgis.PyQt import uic
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtWidgets import QDialog


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
    "MARKERDIALOG_TITLE": [
        "Add Marker",
        "Modify Marker"],
    "MARKERDIALOG_MAINLABEL": [
        "This marker will be created in a new layer.",
        "This marker will be created in layer '{}'.",
        "This marker is located in layer '{}'."],
    "MARKERDIALOG_NOTELABEL":
        "Note:",
    "MARKERDIALOG_INFOLABEL":
        "Comments (optional):",

    # Comment, Remark, Note
    # Annotation, Information, Explanation, Description, Clarification
    # Clarify, Notes, Comments,

    "MARKERDIALOG_NOTEOPTIONS": [
        "Mutation",
        "Correction"
        ]
    })

'''
TODO customisable noteoptions
'''
################################################################################
### Annotation Dialog
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
    _MIN_CHARS = 5
    _MAX_CHARS = 192

    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        # Ensure translated labels
        self.setWindowTitle(_LABELS.MARKERDIALOG_TITLE[0])
        self.mainLabel.setText(_LABELS.MARKERDIALOG_MAINLABEL[0])
        self.noteLabel.setText(_LABELS.MARKERDIALOG_NOTELABEL)
        self.infoLabel.setText(_LABELS.MARKERDIALOG_INFOLABEL)
        self.noteCombo.addItems(_LABELS.MARKERDIALOG_NOTEOPTIONS)

        # Combined textsize should be at least 5 characters,
        # adjust OK button accordingly
        self.noteCombo.currentTextChanged.connect(self.textChanged)
        self.noteCombo.editTextChanged.connect(self.textChanged)
        self.infoText.textChanged.connect(self.textChanged)
        self.updateControls()

    def textChanged(self, text=None):
        self.updateControls()

    def updateControls(self):
        count = len(self.getText())
        valid = self._MIN_CHARS <= count <= self._MAX_CHARS

        button = self.buttonBox.button(self.buttonBox.StandardButton.Ok)
        button.setEnabled(valid)
        txt = str(count)
        txt = txt if valid else txt+' (!)'
        self.sizeLabel.setText(txt)

    ########################################################################
    ### Entrypoint
    ########################################################################

    def askInput(self, layer=None, marker=None):
        # If marker is available, then this is a modify operation
        if marker:
            self.setWindowTitle(_LABELS.MARKERDIALOG_TITLE[1])
            self.setText(marker.note())

        # If layer is available, add layer.name() to mainlabel
        if layer:
            label = _LABELS.MARKERDIALOG_MAINLABEL[1 + bool(marker)]
            label = label.format(layer.name())
            self.mainLabel.setText(label)

        if self.exec():
            return self.getText()

    ########################################################################

    def setText(self, note):
        info = ''
        if ':' in note:
            note, info = note.split(':')
            note = note.strip()
            info = info.strip()
        self.noteCombo.lineEdit().setText(note)
        self.infoText.setPlainText(info)

    def getText(self):
        note = self.noteCombo.currentText()
        info = self.infoText.toPlainText()
        note = note.strip()
        info = info.strip()
        if not note:
            note = info
            info = ''
        if note and info:
            n = 2+len(note)+len(info)
            note += (': ', ':\n')[n>40]
            note += info
        return note



