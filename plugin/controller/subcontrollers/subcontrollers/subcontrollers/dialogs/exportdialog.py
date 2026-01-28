

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QDialog, QFileDialog, QMessageBox


################################################################################
### Labels
################################################################################

import sys
_MODULE = sys.modules.get(__name__.split('.')[0])

_LABELS = _MODULE.LANGUAGE.LABELS({
    "EXPORTDIALOG": {
        "TITLE":
            "Export",
        "LABEL": {
            "LINE1": [
                "You are about to export {} marker from layer '{}'.",
                "You are about to export {} markers from layer '{}'."],
            "LINE2":
                "Select a destination filepath to continue." },
        "PATH": {
            "LABEL":
                "Filepath:" }
        }
    })

_DIALOG = _LABELS.EXPORTDIALOG

################################################################################
### Confirmation Dialog
################################################################################

import os

def _form():
    path, ext = os.path.splitext(__file__)
    form, _ = uic.loadUiType(path+'.ui')
    return form

################################################################################

class Dialog(QDialog, _form()):

    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(_DIALOG.TITLE)
        self.pathLabel.setText(_DIALOG.PATH.LABEL)
        self.pathButton.clicked.connect(self.startBrowser)

        path = os.path.join(os.getcwd(), "export.gpkg")
        self.pathText.setText(path)


    ########################################################################
    ### Entrypoint
    ########################################################################

    def askInput(self, layer=None):
        if layer:
            n = layer.selectedFeatureCount()
            label = _DIALOG.LABEL.LINE1[n>1]
            label += '\n'
            label += _DIALOG.LABEL.LINE2
            label = label.format(n, layer.name())
            self.mainLabel.setText(label)

        if self.exec():
            return self.pathText.text(), "GPKG"

    ########################################################################

    # if browserbutton was clicked, start file-browser
    def startBrowser(self):
        path = self.pathText.text()
        path, format = QFileDialog.getSaveFileName(
        directory=path, filter="GeoPackage (*.gpkg)")
        if path:
            path, ext = os.path.splitext(path)
            if ext.lower() != '.gpkg': ext = '.gpkg'
            self.pathText.setText(path+ext)
