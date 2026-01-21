
import sys
_MODULE = sys.modules.get(__name__.split('.')[0])


from .fsitem import FSFolder

################################################################################
### Database
################################################################################
'''
'''
class Database(FSFolder):
    ITEM_STORAGE_NAME = 'sessions'

    ########################################################################
    ### Central Storage Location
    ########################################################################
    _PATH_KEY = "database/path"

    @classmethod
    def getGlobalPath(cls):
        with _MODULE.plugin.Settings() as settings:
            return settings.loadPath(cls._PATH_KEY)

    @classmethod
    def setGlobalPath(cls, path):
        with _MODULE.plugin.Settings() as settings:
            return settings.savePath(cls._PATH_KEY, path)
    ########################################################################

    def __init__(self, path=None, name=None):
        if not path and not name:
            path = self.getGlobalPath()
        super().__init__(path, name)

    def getSessionSet(self, name=None):
        return FSFolder(self._path, name or self.ITEM_STORAGE_NAME)

