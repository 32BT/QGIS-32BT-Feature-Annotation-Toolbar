

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
    "STORAGEDIALOG_TITLE":
        "Central Storage Location",
    "STORAGEDIALOG_LABEL": [
        "This plugin requires a central storage location.",
        "Please select a storage directory."]
    })

_LABELS.STORAGEDIALOG_LABEL = '\n'.join(_LABELS.STORAGEDIALOG_LABEL)

################################################################################
### Storage Dialog
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

    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(_LABELS.STORAGEDIALOG_TITLE)
        self.mainLabel.setText(_LABELS.STORAGEDIALOG_LABEL)
        self.pathButton.clicked.connect(self.startBrowser)

    def askStorageLocation(self, path=None):
        self.pathText.setText(path or '')
        if self.exec():
            return self.pathText.text().strip()


    # if browserbutton was clicked, start directory-browser
    def startBrowser(self):
        path = self.pathText.text()
        path, name = os.path.split(path)
        options = QFileDialog.Option.ShowDirsOnly
        options |= QFileDialog.Option.DontUseNativeDialog

        dialog = QFileDialog(parent=self, directory=path)
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        dialog.selectFile(name)
        dialog.setNameFilters({'Directories'})
        dialog.setOptions(options)
        if dialog.exec():
            paths = dialog.selectedFiles()
            if paths and paths[0]: self.pathText.setText(paths[0])
'''
This would be convenient, but it shows into the directory,
it does not show the parent directory with the item of interest selected.

    path = QFileDialog.getExistingDirectory(...)
'''

