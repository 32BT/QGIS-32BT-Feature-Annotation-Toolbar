

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
        "LABEL": [
            "You are about to export {} marker from layer '{}'.",
            "You are about to export {} markers from layer '{}'."],
        "FLAG": { "LABEL": "Choose a flag to lock the markers:" },
        "SAVE": { "LABEL": "Select save to choose a destination file." },
        "FILE": { "TYPE": { "CUSTOM": "Other" }}
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
    _LAST_FLAG = 'L'
    _LAST_PATH = os.path.join(os.path.expanduser("~"), 'export.gpkg')

    @classmethod
    def get_lastpath(cls): return cls._LAST_PATH
    @classmethod
    def set_lastpath(cls, path): cls._LAST_PATH = path

    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(_DIALOG.TITLE)
        self.flagLabel.setText(_DIALOG.FLAG.LABEL)
        self.flagText.setText(self._LAST_FLAG)
        self.saveLabel.setText(_DIALOG.SAVE.LABEL)
        button = self.buttonBox.button(self.buttonBox.StandardButton.Save)
        if button: button.setText(button.text()+'...')

    ########################################################################
    ### Entrypoint
    ########################################################################

    def askInput(self, layer=None):
        if layer:
            n = layer.selectedFeatureCount()
            label = _DIALOG.LABEL[n>1]
            label = label.format(n, layer.name())
            self.mainLabel.setText(label)

        if self.exec():
            self.__class__._LAST_FLAG = self.flagText.text()
            # if savebutton was clicked, start file-browser
            path = self.startBrowser()
            if path:
                _, ext = os.path.splitext(path)
                return path, ext[1:], self._LAST_FLAG

    ########################################################################
    '''

    '''
    _FORMATS = {
        ".": _DIALOG.FILE.TYPE.CUSTOM + " (*.*)",
        ".geojson": "GeoJSON (*.geojson)",
        ".gpkg": "GeoPackage (*.gpkg)"}
        # ".gml": "GML (*.gml)"}

    def _get_format(self, ext):
        return self._FORMATS.get(ext.lower()) or self._FORMATS.get(".")

    _EXTENSION = dict(zip(_FORMATS.values(), _FORMATS.keys()))

    def _get_extension(self, format):
        return self._EXTENSION.get(format) or "."
    ########################################################################

    def startBrowser(self, parent=None):
        path = self.get_lastpath()
        _, ext = os.path.splitext(path)

        path, format = QFileDialog.getSaveFileName(
            caption="Export",
            directory=path,
            filter=';;'.join(self._FORMATS.values()),
            initialFilter=self._get_format(ext))
        if path:
            ext = self._get_extension(format)
            if ext != os.path.splitext(path)[-1].lower():
                if ext != ".": path += ext
            self.set_lastpath(path)
            return path


