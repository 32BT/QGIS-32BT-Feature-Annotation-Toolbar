

from ..database.table import FeatureTable
from ..database import Feature
from ..database import LOGFile

'''
ResultTable if a FeatureFolder with the option to merge items from a Layer.
'''

class ResultTable(FeatureTable):

    ########################################################################
    '''
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
