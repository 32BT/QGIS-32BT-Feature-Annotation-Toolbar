

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QDialog, QMessageBox


################################################################################
### Labels
################################################################################

import sys
_MODULE = sys.modules.get(__name__.split('.')[0])

_LABELS = _MODULE.LANGUAGE.LABELS({
    "ARCHIVEDIALOG": {
        "TITLE":
            "Archive",
        "LABEL": {
            "LINE1": [
                "You are about to archive {} marker from layer '{}'.",
                "You are about to archive {} markers from layer '{}'."],
            "LINE2":
                "Confirm this action to continue." },
        "INFOLABEL":
            "Reason:",
        "INFOTEXT":
            "Completed" }
    })

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
        self.setWindowTitle(_LABELS.ARCHIVEDIALOG.TITLE)
        self.infoLabel.setText(_LABELS.ARCHIVEDIALOG.INFOLABEL)
        self.infoText.setText(_LABELS.ARCHIVEDIALOG.INFOTEXT)

    ########################################################################
    ### Entrypoint
    ########################################################################

    def confirmAction(self, layer=None):
        if layer:
            n = layer.selectedFeatureCount()
            label = _LABELS.ARCHIVEDIALOG.MAINLABEL.LINE1[n>1]
            label += '\n'
            label += _LABELS.ARCHIVEDIALOG.MAINLABEL.LINE2
            label = label.format(n, layer.name())
            self.mainLabel.setText(label)

        if self.exec():
            return self.infoText.text().strip()

    ########################################################################


