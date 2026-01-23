

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QDialog, QMessageBox


################################################################################
### Labels
################################################################################

import sys
_MODULE = sys.modules.get(__name__.split('.')[0])

_LABELS = _MODULE.LANGUAGE.LABELS({
    "FREEZEDIALOG": {
        "TITLE":
            "Flag Markers",
        "LABEL": {
            "LINE1": [
                "You are about to flag {} marker from layer '{}'.",
                "You are about to flag {} markers from layer '{}'."],
            "LINE2":
                "Confirm this action to continue." },
        "FLAGLABEL":
            "Flag:",
        "FLAGTEXT":
            "L",
        "FLAGINFO":
            "(Leave empty to remove flag.)"
        }
    })

################################################################################
### Freeze Dialog
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
        self.setWindowTitle(_LABELS.FREEZEDIALOG.TITLE)
        self.flagLabel.setText(_LABELS.FREEZEDIALOG.FLAGLABEL)
        self.flagText.setText(_LABELS.FREEZEDIALOG.FLAGTEXT)
        self.flagInfo.setText(_LABELS.FREEZEDIALOG.FLAGINFO)

    ########################################################################
    ### Entrypoint
    ########################################################################

    def askInput(self, layer=None):
        if layer:
            n = layer.selectedFeatureCount()
            label = _LABELS.FREEZEDIALOG.LABEL.LINE1[n>1]
            label += '\n'
            label += _LABELS.FREEZEDIALOG.LABEL.LINE2
            label = label.format(n, layer.name())
            self.mainLabel.setText(label)

        if self.exec():
            return self.flagText.text().strip()

    ########################################################################


