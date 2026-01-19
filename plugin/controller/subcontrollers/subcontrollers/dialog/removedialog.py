

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QDialog, QMessageBox


################################################################################
### Labels
################################################################################

import sys
_MODULE = sys.modules.get(__name__.split('.')[0])

_LABELS = _MODULE.LANGUAGE.LABELS({
    "CONFIRMDIALOG_TITLE":
        "Confirm Action",
    "CONFIRMDIALOG_MAINLABEL": [
        "You are about to remove {} marker from layer '{}'.",
        "You are about to remove {} markers from layer '{}'."],
    "CONFIRMDIALOG_MAINLABEL2":
        "Confirm this action to continue.",
    "CONFIRMDIALOG_INFOLABEL":
        "Reason:"
    })

################################################################################
### Confirmation Dialog
################################################################################
'''
Pattern:

    result = Dialog(parent).confirmAction(layer)
'''

class Dialog:
    def __init__(self, parent):
        self._parent = parent

    def confirmAction(self, layer):
        title = _LABELS.CONFIRMDIALOG_TITLE
        n = layer.selectedFeatureCount()
        label = _LABELS.CONFIRMDIALOG_MAINLABEL[n>1]
        label += '\n'
        label += _LABELS.CONFIRMDIALOG_MAINLABEL2
        label = label.format(n, layer.name())

        result = \
        QMessageBox.warning(self._parent, title, label,
        QMessageBox.StandardButton.Ok,
        QMessageBox.StandardButton.Cancel)
        return result == QMessageBox.StandardButton.Ok

################################################################################

import os

def _form():
    path, ext = os.path.splitext(__file__)
    form, _ = uic.loadUiType(path+'.ui')
    return form

################################################################################

class _Dialog(QDialog, _form()):

    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(_LABELS.CONFIRMDIALOG_TITLE)
        self.mainLabel.setText(_LABELS.CONFIRMDIALOG_MAINLABEL2)

    ########################################################################
    ### Entrypoint
    ########################################################################

    def confirmAction(self, layer=None):
        if layer:
            n = layer.selectedFeatureCount()
            label = _LABELS.CONFIRMDIALOG_MAINLABEL[n>1]
            label += '\n'
            label += _LABELS.CONFIRMDIALOG_MAINLABEL2
            label = label.format(n, layer.name())
            self.mainLabel.setText(label)

        return self.exec()

    ########################################################################


