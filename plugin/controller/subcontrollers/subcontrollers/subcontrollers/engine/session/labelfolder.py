
from ..database.table import FeatureTable

class LabelFolder(FeatureTable):

    def iconPath(self):
        return self.itemPath('icon.svg')

