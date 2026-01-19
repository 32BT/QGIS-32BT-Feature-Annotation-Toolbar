
from qgis.core import *
from qgis.gui import *
from qgis.PyQt.QtCore import *

################################################################################
### Imports
################################################################################

# Action indices
from .actionscontroller import ACTION

# Actions involve dialogs
from .dialog import MarkerDialog
from .dialog import RemoveDialog

# Require QGS.LAYER and TMS.LAYER functions
from . import qgs as QGS
from . import tms as TMS

# Require MapCanvas utilities
from .qgs.mapcanvas import MapCanvas

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
    ### Validate Action
    ########################################################################

    def updateAction(self, action, idx):
        action.setEnabled(self.validateAction(action, idx))

    def validateAction(self, action, idx):
        # It is not generally sensible to annotate an empty map
        n = len(QgsProject.instance().mapLayers())
        if idx == ACTION.INDEX.RESET: return n>0
        if idx == ACTION.INDEX.APPEND: return n>0
        # Modify and Remove require a selection
        n = self._validateActiveLayer() or 0
        if idx == ACTION.INDEX.MODIFY:
            # Only allow modifying one, unflagged marker at a time
            return n==1 and self._validateActionModify()
        if idx == ACTION.INDEX.REMOVE:
            return n>=1
        return False

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

    def _validateActionModify(self):
        layer = self._iface.activeLayer()
        marker = next(TMS.LAYER.fetch_markers(layer))
        return bool(marker.flag()) == False

    ########################################################################
    ### Handle Action
    ########################################################################

    def handleAction(self, sender, idx):
        if idx == ACTION.INDEX.APPEND:
            location = sender.lastMapLocation
            return self.startAppend(location)
        if idx == ACTION.INDEX.MODIFY:
            return self.startModify()
        if idx == ACTION.INDEX.REMOVE:
            return self.startRemove()

    ########################################################################
    ########################################################################

    def startAppend(self, location):
        print(location)
        layer = self.findLayer()
        note = self.startDialog(layer)
        if note:
            self._addMarker(layer, location, note)

    def startModify(self):
        layer = self._iface.activeLayer()
        marker = next(TMS.LAYER.fetch_markers(layer))
        note = self.startDialog(layer, marker)
        if note and marker.replaceNote(note):
            TMS.LAYER.update_marker(layer, marker)

    def startRemove(self):
        parent = self._iface.mainWindow()
        layer = self._iface.activeLayer()
        if RemoveDialog(parent).confirmAction(layer):
            TMS.LAYER.remove_markers(layer)
    ########################################################################

    def startDialog(self, layer=None, marker=None):
        # Switch active layer to TMS layer and ensure it is visible
        lastActiveLayer = self.setActiveLayer(layer, True)
        # Start dialog
        parent = self._iface.mapCanvas()
        result = MarkerDialog(parent).askInput(layer, marker)
        if result:
            return result
        # User canceled, restore previous active layer
        self.setActiveLayer(lastActiveLayer)

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

    ########################################################################
    ### Save indicator
    ########################################################################
    '''
    If we have a valid annotation, we can create the marker.
    It will be added to layer if it was supplied. If layer is None, we will
    first add an in_memory layer to the toc.
    '''
    def _addMarker(self, layer, mapPoint, note):
        # Create new layer if necessary
        if layer is None:
            name = self.DEFAULT_LAYERNAME
            layer = TMS.LAYER.make(name, self._getMapCrs())
            layer = QGS.LAYER.add_to_toc(layer)
            self._iface.setActiveLayer(layer)

        mapPoint = self._convertMapPoint(mapPoint, layer.crs())

        marker = TMS.Marker(mapPoint, note)
        TMS.LAYER.append_marker(layer, marker)
        # Create indicator and add to layer
        #indicator = TMS.Indicator(mapPoint, txt)
        #TMS.LAYER.appendIndicator(layer, indicator)
        #TMS.LAYER.add_indicator(layer, indicator)

        # set last used layer
        self._layerID = layer.id()

    ########################################################################
    # Helper functions. TODO: move to QGS.MapCanvas

    def mapCanvas(self):
        if not hasattr(self, '_mapCanvas'):
            self._mapCanvas = MapCanvas(self._iface.mapCanvas())
        return self._mapCanvas

    def _convertMapPoint(self, mapPoint, crs):
        return self.mapCanvas().convertMapPoint(mapPoint, crs)

    def _getMapCrs(self):
        return self.mapCanvas().getCrs()
