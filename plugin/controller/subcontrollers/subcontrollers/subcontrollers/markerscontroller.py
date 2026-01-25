
from qgis.core import *
from qgis.gui import *
from qgis.PyQt.QtCore import *

################################################################################
### Imports
################################################################################

# Action indices
from ..actionmanager import ACTION

# Actions involve dialogs
from .dialogs import MarkerDialog
from .dialogs import RemoveDialog
from .dialogs import ArchiveDialog
from .dialogs import FreezeDialog

# Require QGS.LAYER and TMS.LAYER functions
from . import qgs as QGS
from . import tms as TMS

# Require MapCanvas utilities
from .qgs.mapcanvas import MapCanvas

# Require Session for Archive update and handling
from .tms.session import Session

################################################################################
'''
TMS = Token Management System
'''
################################################################################

################################################################################
### Language
################################################################################

import sys
_MODULE = sys.modules.get(__name__.split('.')[0])
_LABELS = _MODULE.LANGUAGE.LABELS({
    "DEFAULT_LAYERNAME": "Markers" })


################################################################################

class MarkersController:

    DEFAULT_LAYERNAME = _LABELS.DEFAULT_LAYERNAME

    def __init__(self, iface):
        self._iface = iface
        self._layerID = None

    ########################################################################
    ### Update Action
    ########################################################################

    def updateAction(self, action, idx):
        action.setEnabled(self.validateAction(action, idx))

    def validateAction(self, action, idx):
        # It is not generally sensible to annotate an empty map
        n = len(QgsProject.instance().mapLayers())
        if idx == ACTION.INDEX.CREATE: return n>0
        # Remaining actions require a selection
        n = self._validateActiveLayer() or 0
        if idx == ACTION.INDEX.MODIFY:
            return n==1 and self._validateActionModify()
        if idx == ACTION.INDEX.DELETE:
            return n>=1 and self._validateActionDelete()
        if idx == ACTION.INDEX.FREEZE:
            return n>=1 and self._validateActionFreeze()
        if idx == ACTION.INDEX.EXPORT:
            return n>=1 and self._validateActionExport()
        if idx == ACTION.INDEX.ARCHIVE:
            return n>=1 and self._validateActionArchive()
        return False

    ########################################################################
    ### Validate Action
    ########################################################################
    '''
    _validateActiveLayer
    --------------------
    Test if active layer is a TMS.LAYER type (with selection).
    If layer is a TMS.LAYER type:
        Return selectedFeatureCount (which might be 0)
    otherwise:
        Return None
    '''
    def _validateActiveLayer(self, mode='w'):
        layer = self._iface.activeLayer()
        if TMS.LAYER.validate(layer, mode):
            return layer.selectedFeatureCount()

    # Only allow unflagged items to be modified
    def _validateActionModify(self):
        layer = self._iface.activeLayer()
        marker = next(TMS.LAYER.fetchMarkers(layer))
        return bool(marker.flag()) == False

    # Only allow unflagged items in a deleteset
    def _validateActionDelete(self):
        layer = self._iface.activeLayer()
        for marker in TMS.LAYER.fetchMarkers(layer):
            if marker.flag(): return False
        return True

    # TODO: unfreeze?
    def _validateActionFreeze(self):
        return True

    # Any selectionset can be exported
    def _validateActionExport(self):
        return True

    # Allow archive if layer is sessionlayer
    def _validateActionArchive(self):
        layer = self._iface.activeLayer()
        return Session.validate_layer(layer)

    ########################################################################
    ### Handle Action
    ########################################################################

    def handleAction(self, sender, idx):
        if idx == ACTION.INDEX.CREATE:
            return self.startAppend()
        if idx == ACTION.INDEX.MODIFY:
            return self.startModify()
        if idx == ACTION.INDEX.DELETE:
            return self.startRemove()
        if idx == ACTION.INDEX.FREEZE:
            return self.startFreeze()
        if idx == ACTION.INDEX.ARCHIVE:
            return self.startArchive()

    ########################################################################

    def startAppend(self):
        layer = self.findLayer()
        note = self.runInputDialog(layer)
        if note:
            layer = self.assertLayer(layer)
            layerPoint = self._getLastEventLocation(layer.crs())
            # WARNING: A rather broad assumption...
            if layer.crs().mapUnits() == QgsUnitTypes.DistanceMeters:
                layerPoint = TMS.Marker.class_round(layerPoint, 3)
            # END-OF-WARNING
            marker = TMS.Marker(layerPoint, note)
            print(marker.as_json())
            TMS.LAYER.appendMarker(layer, marker)
            self._layerID = layer.id()

    def startModify(self):
        layer = self._iface.activeLayer()
        marker = next(TMS.LAYER.fetchMarkers(layer))
        note = self.runInputDialog(layer, marker)
        if note and marker.replaceNote(note):
            TMS.LAYER.updateMarker(layer, marker)
            self._layerID = layer.id()

    def startRemove(self):
        layer = self._iface.activeLayer()
        if self.runRemoveDialog(layer):
            TMS.LAYER.removeMarkers(layer)
            self._layerID = layer.id()

    ########################################################################

    def startFreeze(self):
        layer = self._iface.activeLayer()
        flag = self.runFreezeDialog(layer)
        if flag is not None:
            TMS.LAYER.freezeMarkers(layer, flag)
            layer.removeSelection()

    def startArchive(self):
        layer = self._iface.activeLayer()
        reason = self.runArchiveDialog(layer)
        if reason:
            TMS.LAYER.removeMarkers(layer, reason)
            self._layerID = layer.id()

    ########################################################################
    ########################################################################

    def runInputDialog(self, layer=None, marker=None):
        # Switch active layer to TMS layer and ensure it is visible
        lastActiveLayer = self.setActiveLayer(layer, True)
        # Start dialog
        result = self.runMarkerDialog(layer, marker)
        if result: return result
        # User canceled, restore previous active layer
        self.setActiveLayer(lastActiveLayer)

    def runMarkerDialog(self, layer=None, marker=None):
        parent = self._iface.mapCanvas()
        return MarkerDialog(parent).askInput(layer, marker)

    def runRemoveDialog(self, layer):
        parent = self._iface.mapCanvas()
        return RemoveDialog(parent).confirmAction(layer)

    def runFreezeDialog(self, layer):
        parent = self._iface.mapCanvas()
        return FreezeDialog(parent).askInput(layer)

    def runArchiveDialog(self, layer):
        parent = self._iface.mapCanvas()
        return ArchiveDialog(parent).confirmAction(layer)

    ########################################################################
    ### Layer management
    ########################################################################
    '''
    The plugin requires a targetlayer that can handle markers.

    Strategy for determining valid targetlayer:
        First check currently active layer,
        otherwise check last used layer,
        otherwise check any layer,
        otherwise start new layer.

    NOTE: a mapped layer is considered a valid TMS layer (for sending),
    but might not be editable. We want to add an indicator, so we need
    an editable TMS layer.
    '''
    def findLayer(self):
        # First check currently active layer
        layer = self._iface.activeLayer()
        if TMS.LAYER.validate(layer, 'w'): # validate for write
            return layer

        # otherwise check last used layer (might be None)
        layer = QGS.LAYER.find_in_toc(self._layerID)
        if TMS.LAYER.validate(layer, 'w'): # validate for write
            return layer

        # otherwise check all visible layers for first editable valid layer
        # (from treetop to bottom, not random...)
        root = QgsProject.instance().layerTreeRoot()
        for layer in root.checkedLayers():
            if QGS.LAYER.is_visible(layer):
                if TMS.LAYER.validate(layer, 'w'):
                    return layer

        # otherwise trigger new layer
        return None

    '''
    If targetlayer already exists, then it should be active and visible prior to
    starting the dialog for a new marker. This will allow the user to validate
    the necessity of the marker first, and will provide feedback if the marker
    is eventually added later.
    This method returns the previously active layer so that the active layer
    can be reset on cancel.
    '''
    def setActiveLayer(self, layer, forceVisible=False):
        lastLayer = self._iface.activeLayer()
        if layer is not None:
            self._iface.setActiveLayer(layer)
            if forceVisible:
                QGS.LAYER.make_visible(layer)
        return lastLayer

    '''
    If there is no layer, then create an ad-hoc, in-memory layer.
    '''
    def assertLayer(self, layer):
        if layer is None:
            name = self.DEFAULT_LAYERNAME
            layer = TMS.LAYER.make(name, self._getMapCrs())
            layer = QGS.LAYER.add_to_toc(layer)
            self._iface.setActiveLayer(layer)
        return layer

    ########################################################################
    # Helper functions.
    def mapCanvas(self):
        if not hasattr(self, '_mapCanvas'):
            self._mapCanvas = MapCanvas(self._iface.mapCanvas())
        return self._mapCanvas

    def _convertMapPoint(self, mapPoint, crs):
        return self.mapCanvas().convertMapPoint(mapPoint, crs)

    def _getLastEventLocation(self, crs=None):
        return self.mapCanvas().getLastEventLocation(crs)

    def _getMapCrs(self):
        return self.mapCanvas().getCrs()
