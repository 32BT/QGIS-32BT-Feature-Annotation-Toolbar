

from qgis.core import QgsMessageLog, Qgis


def LOG(*S):
    S = [str(s) for s in S]
    QgsMessageLog.logMessage(' '.join(S), '32BT', Qgis.Info)


################################################################################
### Sentinel
################################################################################
'''
In order to prepopulate a sessionlayer with features, we use a sentinelobject.

A sessionlayer is usually created as a memorylayer. If a sessionlayer was saved
with the project, it remains a memory layer which will be empty when reopening
the projectfile.

Sentinel object therefore checks if a sessionlayer was added and, if so,
whether it has features. If not, it will add the features from the session
itemfolder and any additional tables.

NOTE:
    There are several signals available, but they behave counterintuitively.
    -- QgsProject.instance().layersAdded --
    Contrary to what the name suggests it behaves functionally equivalent to
    -- QgsProject.instance().layerWasAdded --
    They will both be called for each layer when it has loaded, NOT added,
    because, contrary to what both signalnames suggest, the layer reported is
    NOT available in the mapLayers list, and lacks joinlayers if applicable.

    mapCanvas.layersChanged does work, but will also be called for minor
    changes like visibility switches. We do not need to traverse the entire
    list of layers each time the visibility is changed for a layer.

'''
from qgis.core import QgsProject
from qgis.PyQt.QtCore import QTimer, Qt

from .session import Session

class Sentinel:
    def __init__(self, iface=None):
        self._iface = iface
        QgsProject.instance().layerWasAdded.connect(self.layerWasAdded)
        '''
        If plugin was just activated, we need to check any existing layers in
        the mapLayers list. Since we might be activated in the PluginManager,
        we need to allow gui some time to update before starting a potentially
        slightly longish action. ("longish" meaning: not quite long enough
        to merrit a true backgroundproces.)
        '''
        QTimer.singleShot(100, Qt.TimerType.CoarseTimer, self.addLayers)

    def addLayers(self):
        for layer in QgsProject.instance().mapLayers().values():
            self.layerWasAdded(layer)

    def layerWasAdded(self, layer):
        path = Session.get_path(layer)
        if path and not layer.hasFeatures():
            print("layerWasAdded:", layer.name())
            Session(path).refreshLayer(layer)

