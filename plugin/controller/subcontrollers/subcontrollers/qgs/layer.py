
from qgis.core import *
from qgis.PyQt.QtCore import QMetaType

################################################################################
'''
Layers, especially temporary layers, can be part of the mapregistry, while not
being part of the toc.
find_in_map searches all layers
find_in_toc searches toc layers
'''
# Find layer in registry
def find_in_map(_id):
    return QgsProject.instance().mapLayer(_id)

# Find layer in ToC
def find_in_toc(_id):
    root = QgsProject.instance().layerTreeRoot()
    if root:
        node = root.findLayer(_id)
        if node:
            return node.layer()

# Add layer to toc
def add_to_toc(layer, index=0):
    if not find_in_toc(layer.id()):
        if not find_in_map(layer.id()):
            layer = QgsProject.instance().addMapLayer(layer, False)
    root = QgsProject.instance().layerTreeRoot()
    root.insertLayer(index, layer)
    return layer


def make_visible(layer):
    root = QgsProject.instance().layerTreeRoot()
    if root:
        node = root.findLayer(layer.id())
        if node:
            node.setItemVisibilityCheckedParentRecursive(True)

################################################################################

def validate(layer):
    return bool(layer) and layer.isValid()

def validate_storagetype(layer, storageType='memory'):
    return layer.storageType().lower().startswith(storageType.lower())

def set_skipcheck(layer, skipCheck=True):
    layer.setCustomProperty("skipMemoryLayersCheck", skipCheck)



# Redundant version of validate
def is_valid(layer):
    return bool(layer) and layer.isValid()

# Whether layer and its containers are all checked
def is_visible(layer):
    if layer:
        root = QgsProject.instance().layerTreeRoot()
        if root:
            node = root.findLayer(layer.id())
            if node:
                return node.isVisible()
    return False

# Whether this layer is checked, regardless of container visibility
def is_checked(layer):
    if layer:
        root = QgsProject.instance().layerTreeRoot()
        if root:
            node = root.findLayer(layer.id())
            if node:
                return node.itemVisibilityChecked()
    return False



def is_editable(layer):
    try:
        C = layer.dataProvider().capabilities()
        return C & QgsVectorDataProvider.AddFeatures
    except AttributeError:
        return False


################################################################################

def validate_geometry(layer, geometryType=Qgis.GeometryType.Point):
    return (hasattr(layer, 'geometryType') and
    layer.geometryType() == geometryType)

def validate_pointgeometry(layer):
    return validate_geometry(layer)



'''
add_feature will adapt feature before calling addFeature
'''
def add_feature(layer, feature):
    if feature.fields().names() != layer.fields().names():
        feature = feature_with_fields(feature, layer.fields())
    addFeature(layer, feature)
    return feature

def feature_with_fields(feature, fields):
    F = QgsFeature(fields)
    F.setGeometry(feature.geometry())
    for f in fields.names():
        try: F[f] = feature[f]
        except KeyError: pass
    return F

################################################################################
'''
'''
def set_value(layer, fid, key, val, size=32):
    if not hasAttribute(layer, key):
        addAttribute(layer, key, size)
    feature = layer.getFeature(fid)
    feature[key] = val
    updateFeature(layer, feature)


def addFields(layer, fields):
    for field in fields:
        if not hasAttribute(layer, field.name()):
            addField(layer, field)

def addField(layer, field):
    with edit(layer):
        layer.addAttribute(field)

def hasAttribute(layer, name):
    return name in layer.fields().names()

def addAttribute(layer, name, size=32):
    field = QgsField(name, QMetaType.QString, typeName='text', len=size)
    addField(layer, field)

################################################################################

def addFeature(layer, feature):
    with edit(layer):
        layer.addFeature(feature)
        layer.selectByIds([feature.id()])

def addFeatures(layer, features):
    layer.removeSelection()
    with edit(layer):
        for feature in features:
            layer.addFeature(feature)

def updateFeature(layer, feature):
    with edit(layer):
        layer.updateFeature(feature)

def deleteFeature(layer, fid):
    with edit(layer):
        layer.deleteFeature(fid)

def deleteFeatures(layer, fids):
    layer.removeSelection()
    with edit(layer):
        layer.deleteFeatures(fids)

################################################################################
'''
'''
class Layer:
    def __init__(self, layer):
        self._id = layer.id()

    def as_qgislayer(self):
        return QgsProject.instance().mapLayer(self._id)

    def addFeature(self, f):
        self.updateFields(f.fields())
        layer = self.as_qgislayer()
        if layer: addFeature(layer, f)

    def updateFeature(self, f):
        self.updateFields(f.fields())
        layer = self.as_qgislayer()
        if layer: updateFeature(layer, f)

    def updateFields(self, fields):
        layer = self.as_qgislayer()
        if layer: addFields(layer, fields)

    def setValue(self, fid, key, val, size=32):
        layer = self.as_qgislayer()
        if layer: set_value(layer, fid, key, val, size)
