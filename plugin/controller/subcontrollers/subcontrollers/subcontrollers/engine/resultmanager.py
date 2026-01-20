
import os
from qgis.core import *

from .resultlayer import Layer, TableLayer, ResultLayer
from .session import SessionFolder

from . import _qgs as QGS
from .database import Feature
from .database.table import FeatureTable
from .database import FSItem, LOGFile, CSVFile


################################################################################
### ResultManager
################################################################################
'''
Ingredients:
    sourceLayer  --> Layer (or None?)
    resultLayer  --> Layer
    ResultLog    --> CSVFile
    ResultFile   --> CSVFile
    ResultTable  --> FeatureFolder
    LabelsFolder --> LabelsFolder

Structure:
    sourceLayer --> Layer (or None?)
    resultLayer --> Layer
    resultFolder --> SessionFolder
        logFile      --> CSVFile
        lyrFile      --> CSVFile
        labelsFolder --> LabelsFolder
        featureTable --> FeatureTable


If a source layer is available and has an exclusive selection, the items
will be copied to results including a label and optionally a comment.
Alternatively, if the result layer has an exclusive selection, its items
will be updated with the new results.

This allows a preselection to be made and saved in the ResultTable.
'''

################################################################################
################################################################################
'''
We are going to stuff following objects in ItemController:
    ResultLayer <--
    ResultTable <--
    ResultLog (requires guid/label not guid/feat)
    ResultFile (requires guid/label not guid/feat)
    LabelsFolder (requires label/guid/feat)

Every object in ItemController will receive the guid,feat combo.
ResultLayer and ResultTable will eat that straight.
ResultLog, ResultFile, and LabelsFolder require a translation:
'''
'''
from .session import ResultLog as _ResultLog
from .session import ResultFile as _ResultFile
from .session import LabelsFolder as _LabelsFolder

class ResultLog(_ResultLog):
    def __setitem__(self, guid, feat):
        label = feat['label']
        super().__setitem__(guid, label)

class ResultFile(_ResultFile):
    def __setitem__(self, guid, feat):
        label = feat['label']
        super().__setitem__(guid, label)

class LabelsFolder(_LabelsFolder):
    def __setitem__(self, guid, feat):
        label = feat['label']
        super().__setitem__(label, (guid, feat))

'''

################################################################################
### Sentinel
################################################################################
'''
In order to prepopulate a sessionlayer with features, we use a sentinelobject
to listen for layer-load signals.
'''
'''
class Sentinel:
    _key = "fct/session/layer/sentinel"

    def __init__(self):
        project = QgsProject.instance()
        if not project.property(self._key):
            project.setProperty(self._key, self)
            project.layerWasAdded.connect(self.layerWasAdded)
            for layer in project.mapLayers().values():
                layerWasAdded(layer)

    def layerWasAdded(self, layer):
        if ResultManager.validate_layer(layer):
            print('fct session layer added:', layer.name(), layer.storageType())
            if TableLayer.validate_storagetype(layer, 'memory'):
                if not layer.hasFeatures():
                    TableLayer(layer).refresh()


#Sentinel()
'''

################################################################################

class ResultManager:
    ########################################################################
    _SESSION_PATH_KEY = "fct/session/path"

    @classmethod
    def validate_layer(cls, layer):
        return bool(layer.customProperty(cls._SESSION_PATH_KEY))

    @classmethod
    def get_session_path(cls, layer):
        path = layer.customProperty(cls._SESSION_PATH_KEY)
        if path: return FSItem.path_expanduser(path)

    @classmethod
    def set_session_path(cls, layer, path):
        path = FSItem.path_shrinkuser(path)
        layer.setCustomProperty(cls._SESSION_PATH_KEY, path)

    @classmethod
    def find_session_layer(cls, path):
        for layer in QgsProject.instance().mapLayers().values():
            if path == cls.get_session_path(layer): return layer

    ########################################################################
    '''
    SourceLayer guid field name
    '''
    _SESSION_GUID_KEY = "fct/session/guid"

    @classmethod
    def get_session_guid(cls, layer):
        return layer.customProperty(cls._SESSION_GUID_KEY)

    @classmethod
    def set_session_guid(cls, layer, guid):
        layer.setCustomProperty(cls._SESSION_GUID_KEY, guid)

    ########################################################################
    '''
    fromLayer means we are dealing with an existing resultLayer, and user
    wants to activate it as a session.
    '''
    @classmethod
    def fromLayer(cls, layer):
        session_path = cls.get_session_path(layer)
        field = layer.fields().names()[0]
        sessionFolder = SessionFolder(session_path, field=field).start()
        sourceLayer = Layer(layer)
        resultLayer = ResultLayer(layer)
        resultLayer.selectUnparsedItems()
        return cls(sessionFolder, sourceLayer, resultLayer)

    '''
    fromSettings means user wants a new session, regardless of whether
    sourceLayer is itself a resultLayer.
    '''
    @classmethod
    def fromSettings(cls, layer, settings):
        session_path, field = settings.path(), settings._fld
        sessionFolder = SessionFolder(session_path, field=field).start()

        sourceLayer = Layer(layer, field)
        if sourceLayer.selectedFeatureCount() > 0:
            sessionFolder.featureTable.mergeSelectedItems(sourceLayer)

        table_path = sessionFolder.featureTablePath()
        resultLayer = ResultLayer.start(table_path, sourceLayer.layer(), field)
        cls.set_session_path(resultLayer.layer(), session_path)
        # If style is present, override default style
        path = sessionFolder.stylePath()
        if path: resultLayer.applyStyle(path)
        # Add to toc and skip check
        resultLayer.addToMap(True, True)

        return cls(sessionFolder, sourceLayer, resultLayer)


    def __init__(self, sessionFolder, sourceLayer, resultLayer):
        # _joined is used in __del__, set it before anything else!
        self._joined = False
        self._toc = True # TODO:

        if sourceLayer is None:
            sourceLayer = resultLayer

        self._sourceLayer = sourceLayer
        self._resultLayer = resultLayer
        self._resultSession = sessionFolder


    def __del__(self):
        print('ResultSession.__del__')
        if self._joined:
            self._detachLayers()

    ########################################################################
    ########################################################################
    '''
    We can not attach a new resultlayer unless a previous resultlayer has
    first been removed, since they use the same headers.

    TODO: maybe search joined layers and remove any previous connection
    '''
    def startup(self):
        if self._toc == False:
            self._attachLayers()

    def cleanup(self):
        self._detachLayers()

    def _attachLayers(self):
        if self._joined == False:
            sourceLayer = self._sourceLayer
            resultLayer = self._resultLayer
            resultLayer.attachTo(sourceLayer)
            self._joined = True

    def _detachLayers(self):
        if self._joined == True:
            sourceLayer = self._sourceLayer
            resultLayer = self._resultLayer
            resultLayer.detachFrom(sourceLayer)
            self._joined = False

    ########################################################################


    def sourceLayer(self):
        return self._sourceLayer

    def sourceLayerID(self):
        return self._sourceLayer.id()

    def resultLayer(self):
        return self._resultLayer

    def resultLayerID(self):
        if self._resultLayer:
            return self._resultLayer.id()

    def resultLayerInList(self, idList):
        if self._resultLayer:
            return self._resultLayer.id() in idList
        return False

    ########################################################################
    ########################################################################
    '''
    A labelsession should allow exclusive selection only, in either
    source or result, but not in both at the same time.
    '''
    def selectedFeaturesChanged(self, layer):
        if self._sourceLayer != self._resultLayer:
            if self._sourceLayer == layer and layer.selectedFeatureCount():
                self._resultLayer.layer().removeSelection()
            if self._resultLayer == layer and layer.selectedFeatureCount():
                self._sourceLayer.layer().removeSelection()

    ########################################################################
    '''
    The internal Layer class compares layer ids, and can therefore compare
    itself with a qgis layer.

    Label buttons will be activated if:
        - there is a selection in one of our session layers.

    This does not necessarily allow labeling, but it allows us to warn user
    in case of ambiguity in selection.
    '''
    def __contains__(self, layer):
        if layer and layer.isValid():
            if self._sourceLayer == layer: return True
            if self._resultLayer == layer: return True
        return False

    def validateLayer(self, layer):
        return (
        (self._sourceLayer.selectedFeatureCount() > 0) or
        (self._resultLayer.selectedFeatureCount() > 0))

    def validateSelection(self):
        srcN = self._sourceLayer.selectedFeatureCount()
        dstN = self._resultLayer.selectedFeatureCount()
        if srcN+dstN == 0: return False
        return ((srcN > 0) != (dstN > 0) or
        self._sourceLayer == self._resultLayer)

    ########################################################################
    '''
    Used by labelcontroller in setResultMgr_ea
    TODO:
    '''
    def qgis_source_layer(self):
        return self._sourceLayer.layer()
    ########################################################################

    def labelInfo(self):
        return self._resultSession.labelInfo()


    # TODO: strategy for updating features that include comment?
    def findComments(self):
        comments = []
        fids = self._sourceLayer.selectedFeatureIds()
        for fid in fids:
            srcFeature = self._sourceLayer.getFeature(fid)
            if srcFeature and srcFeature.isValid():
                guid = srcFeature[self._fld]
                feat = self._labelSession.getFeature(guid)
                if feat:
                    comment = feat.get('comment')
                    if comment and comment not in comments:
                        comment.append(comment)
        if len(comments)>1:
            comments.insert(0, "Warning: multiple comments found!")
        return "\n\n".join(comments)

    ########################################################################
    ########################################################################
    '''
    userclick --> labelController --> setLabel

    After user clicks a labelbutton, the labelController will call setLabel.
    If the alt-key was pressed, this will include a comment.
    '''
    def setLabel(self, label, comment=None):
        # Either sourceLayer or resultLayer has selection
        if self._sourceLayer.selectedFeatureCount() > 0:
            self._setLabel(self._sourceLayer, label, comment)
        else:
            self._setLabel(self._resultLayer, label, comment)

    '''
    sourceLayer --> timestamped copy --> featureTable

    Items are timestamped with a date. This reflects the date of copying the
    shape from its original source to the resultFolder. If the Session has
    its source set to its own resultFolder, then the items are not copied,
    and the date should not change.
    '''
    def _setLabel(self, layer, label, comment=None):
        for guid, item in layer.selectedItems():
            # Set copy date to now, unless item comes from result
            date = LOGFile.get_date()
            if layer == self._resultLayer:
                date = item['date'] or date
            item.properties = {}
            item['date'] = date
            item['label'] = label
            item['comment'] = comment
            self._setResultItem(guid, item)

    '''
    A result is saved if it is new, or has updates other than timestamp.
    (Note: resultLayer also contains guid, new features do not.)
    '''
    _KEY_UPDATES = ('label', 'comment', 'shape')

    def _setResultItem(self, guid, feat):
        # Set feat if new or changed
        item = self._resultLayer[guid]
        if not item or item.keyDifferences(feat, self._KEY_UPDATES):
            self._resultLayer[guid] = feat
            self._resultSession[guid] = feat







