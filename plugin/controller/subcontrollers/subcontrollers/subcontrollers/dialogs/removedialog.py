

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QDialog, QMessageBox


################################################################################
### Labels
################################################################################

import sys
_MODULE = sys.modules.get(__name__.split('.')[0])

_LABELS = _MODULE.LANGUAGE.LABELS({
    "REMOVEDIALOG": {
        "TITLE":
            "Delete",
        "LABEL": {
            "LINE1": [
                "You are about to remove {} marker from layer '{}'.",
                "You are about to remove {} markers from layer '{}'."],
            "LINE2":
                "Confirm this action to continue."
            }
        }
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
        title = _LABELS.REMOVEDIALOG.TITLE
        n = layer.selectedFeatureCount()
        label = _LABELS.REMOVEDIALOG.LABEL.LINE1[n>1]
        label += '\n'
        label += _LABELS.REMOVEDIALOG.LABEL.LINE2
        label = label.format(n, layer.name())

        result = \
        QMessageBox.warning(self._parent, title, label,
        QMessageBox.StandardButton.Ok,
        QMessageBox.StandardButton.Cancel)
        return result == QMessageBox.StandardButton.Ok

################################################################################

