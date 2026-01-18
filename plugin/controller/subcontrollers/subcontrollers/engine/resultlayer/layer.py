

from qgis.core import *
from qgis.PyQt.QtCore import *

from ..database import FSFile, LOGFile, Feature

################################################################################
### Layer
################################################################################
'''
Layer is a controllerobject for an application-specific layer.
It is meant as a translation between that layer and our internal logic.
Our internal logic uses the internal Feature class and assumes more
flexible layers. Layer will adapt to incoming Feature properties.

Class hierarchy:

      Layer
        |
        V
    TableLayer (Layer with tablepath property)
        |
        V
    ResultLayer


Features can be added using dictionary logic.

    layer[guid] = feature
    This will add feature as a qgis-feature to the qgis-layer using guid as id.
    If an entry with guid already exists, it will be updated. If necessary,
    the layer will be adapted to accommodate the feature properties.

    feature = layer[guid]
    This will return a feature for the first qgis-feature found with guid.
    This will return None if there is no qgis-feature with guid.
    It will not raise a LookupError.

    del layer[guid]
    This will remove all entries with guid.

Note:
A qgis layer is a wrapper object. It can not be referenced after removal.
However, to reduce unnecessary double-triple checks and code-size, it is
assumed that a higher-level controller will properly respond to
layersWillBeRemoved, and dispense the use of this Layer controller.
'''

class Layer:
    def __init__(self, layer, field=0):
        super().__init__()
        self._layer = layer
        self._field = field

    def layer(self):
        return self._layer

    ########################################################################
    ### QGIS compatibility
    ########################################################################
    '''
    Layer needs a minimal set of qgis layer functions so we can use a Layer
    where a qgis-layer would be expected.
    '''

    def id(self):
        return self._layer.id()

    def __eq__(self, layer):
        return self.id()==layer.id()

    def selectedFeatureCount(self):
        return self._layer.selectedFeatureCount()

    ########################################################################
    ### Startup
    ########################################################################
    '''
    Following functions are called during initialisation or right after.
    Layer generally represents a temporary layer that can be reloaded
    easily after a restart. By default it will skip memorylayerscheck.
    Skipping the check can be set by the skipMemoryLayersCheck custom property,
    which is set in addToMap below.
    '''
    def refresh(self, items=[]):
        with edit(self._layer):
            self._removeAll()
            for guid, feature in items:
                self._append(guid, feature)

    def applyStyle(self, path):
        if FSFile.validate_path(path):
            self._layer.loadNamedStyle(path,
            flags=Qgis.LoadStyleFlag.IgnoreMissingStyleErrors)
            return True
        return False

    def addToMap(self, visible=True, skipCheck=True):
        layer = self._layer
        layer.setCustomProperty("skipMemoryLayersCheck", skipCheck)
        return QgsProject.instance().addMapLayer(layer, visible)

    ########################################################################
    ### Entry management
    ########################################################################

    def __contains__(self, guid):
        feature = self._find(guid)
        return True if feature else False

    def __setitem__(self, guid, item):
        self.setItem(guid, item)

    def __getitem__(self, guid):
        return self.getItem(guid)

    def __delitem__(self, guid):
        self.deleteItem(guid)

    # Add new entry or update existing entry
    def setItem(self, guid, item):
        # deferred editing also triggers all reload actions
        with edit(self._layer):
            self._update(guid, item)

    def getItem(self, guid):
        qgis_feature = self._find(guid)
        if qgis_feature:
            return Feature.from_qgis_feature(qgis_feature)

    def deleteItem(self, guid):
        with edit(self._layer):
            return self._remove(guid)

    ########################################################################
    ### Mimic dict / ItemController
    ########################################################################
    '''
    We use ArcGIS logic: iterate selection if available, otherwise iterate all
    '''
    def __iter__(self):
        for feat in self._get_qgis_features():
            yield feat[self._field]

    def keys(self):
        for feat in self._layer.getFeatures():
            yield feat[self._field]

    def items(self):
        return self._get_features(self._layer.getFeatures())

    def selectedItems(self):
        return self._get_features(self._layer.selectedFeatures())

    def _get_features(self, qgis_features):
        for feat in qgis_features:
            guid = feat[self._field]
            feat = Feature.from_qgis_feature(feat)
            yield guid, feat

    def _get_qgis_features(self):
        layer = self._layer
        if layer.selectedFeatureCount()>0:
            return layer.selectedFeatures()
        return layer.getFeatures()

    ########################################################################
    '''
    If layer has active featureTable, then this can be used to merge src items.
    '''
    def mergeSelectedItems(self, srcLayer, attributes=[]):
        if attributes is None: attributes = srcLayer.attributeNames()
        dstItems = set(self.keys())
        for guid, feat in srcLayer.selectedItems():
            if guid not in dstItems:
                prps = feat.properties
                feat.properties = dict(date=LOGFile.get_date())
                for key in attributes: feat[key] = prps[key]
                self[guid] = feat

    ########################################################################
    ### Lower level functions
    ########################################################################
    '''
    Lower level functions are meant to be called by self, not by outsiders.
    '''
    def _fieldName(self):
        if isinstance(self._field, int):
            return self.attributeName(self._field)
        return self._field

    def _find(self, guid):
        for feat in self._layer.getFeatures():
            if feat[self._field] == guid: return feat

    def _findShape(self, shape):
        for feat in self._layer.getFeatures():
            raise NotImplementedError('_findShape')


    def _remove(self, guid):
        feature = self._find(guid)
        if feature:
            self._layer.deleteFeature(feature.id())
            return True
        return False

    def _removeAll(self):
        fids = self._layer.allFeatureIds()
        if fids: self._layer.deleteFeatures(fids)

    '''
    If we receive an internal-type Feature:
    We adapt layer to accommodate feature as best as possible.
        new attributes = feature_properties - layer_attributes
        extend layer_attributes with any new attribute if possible

    Then we create a QgsFeature compatible with layer_attributes,
    and add it to the qgis-layer.

    '''
    def _prepare(self, guid, feature):
        self._prepare_layer(feature)
        feat = self._create_qgis_feature(feature)
        if not feat[0]: feat[0] = guid
        return self._prepare_qgis_feature(feat)

    def _append(self, guid, feature):
        feat = self._prepare(guid, feature)
        self._append_feature(feat)

    def _update(self, guid, feature):
        feat = self._prepare(guid, feature)
        self._update_layer(guid, feat)

    ########################################################################
    '''
    Note that we need true update, since a replace will change feature ids
    within the layer. That will confuse the navigationcontroller if it is
    navigating this layer.
    '''

    def _update_layer(self, guid, feat):
        found_feature = self._find(guid)
        if not found_feature:
            self._append_feature(feat)
        else:
            self._update_feature(found_feature.id(), feat)

    def _append_feature(self, feat):
        self._layer.addFeature(feat)

    '''
    TODO: probably move to QGS.LAYER(layer).updateFeature(fid, feat)
    Not really sure why this would be faster than updateFeature as per docs,
    however: it's really bad form to change the id of an incoming parameter,
    and it's also crazy to copy a feature object for just that purpose.
    '''
    def _update_feature(self, fid, feat):
        self._layer.changeGeometry(fid, feat.geometry())
        values = feat.attributes()
        values = dict(enumerate(values))
        self._layer.changeAttributeValues(fid, values)

    ########################################################################
    ### Matching attributes
    ########################################################################
    '''
    Layer may not initially match all feature properties.
    We allow some default fields to be added dynamically, e.g.:
    - Layer does not initially have a comment column.
    - Most Features will also lack a comment property.
    - The first feature that includes a comment, will expand the layer-fields.
    '''

    # if necessary, extend layer-attributes to accommodate feature properties
    def _prepare_layer(self, feature):
        keys = list(feature.properties.keys())
        keys = self.attributeNames()+keys
        keys = list(dict.fromkeys(keys))
        for key in keys[self.attributeCount():]:
            self.addTextAttribute(key)

    def _create_qgis_feature(self, feature):
        return feature.as_qgis_feature(self.attributes())

    # Allow subclasses to adjust feature
    def _prepare_qgis_feature(self, feature):
        return feature

    ########################################################################
    ### Attribute Management
    ########################################################################
    '''
    For unknown reasons, a layer's field is also referred to as attribute.
    So, for consistency and ease-of-access:
    '''
    def attributes(self):
        return self._layer.fields()

    def attributeCount(self):
        return self._layer.fields().count()

    def attributeNames(self):
        return self._layer.fields().names()

    def attributeName(self, idx=0):
        return self.attributeNames()[idx]

    def addTextAttribute(self, name, size=None):
        if size is None: size = self._defaultSizeForAttribute(name)
        field = QgsField(name, QMetaType.QString, typeName='text', len=size)
        self._layer.addAttribute(field)

    def _defaultSizeForAttribute(self, name):
        if name == 'guid': return 64
        if name in ('note', 'comment'): return 128
        return 32
