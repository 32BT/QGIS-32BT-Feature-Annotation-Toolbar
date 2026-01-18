################################################################################
### Settings
################################################################################
'''
For privacy reasons we should store relative paths in settings.
'''
import os

def os_path_shrinkuser(path):
    home = os.path.expanduser('~')
    if home and path.startswith(home):
        path = '~'+path[len(home):]
    return path

################################################################################


from qgis.core import QgsSettings

class PluginSettings(QgsSettings):

    def __init__(self, pluginName='fct'):
        super().__init__()
        self._pluginName = pluginName

    def __enter__(self):
        # start with group '32bt' which will create a section [32bt]
        # (add section=self.Plugins if it needs to go in section [plugins])
        self.beginGroup('32bt')
        self.beginGroup(self._pluginName)
        return self

    def __exit__(self, *args):
        self.endGroup()
        self.endGroup()
        self.sync()

    ########################################################################
    # save dictionary k,v pairs under groupname key
    def saveGroup(self, key, dct):
        self.remove(key)
        self.beginGroup(key)
        try:
            self.saveGroupValues(dct)
        finally:
            self.endGroup()

    def loadGroup(self, key):
        self.beginGroup(key)
        try:
            return self.loadGroupValues()
        finally:
            self.endGroup()

    ########################################################################

    def saveGroupValues(self, dct):
        for key,val in dct.items():
            if isinstance(val, dict):
                self.saveGroup(key, val)
            else:
                self.saveValue(key, val)

    def loadGroupValues(self):
        D = {}
        for key in self.childKeys():
            D[key] = self.loadValue(key)
        for key in self.childGroups():
            D[key] = self.loadGroup(key)
        return D

    ########################################################################
    def savePath(self, key, path):
        self.saveValue(key, os_path_shrinkuser(path))

    def loadPath(self, key):
        return os.path.expanduser(self.loadValue(key))
    ########################################################################
    def saveValue(self, key, val):
        self.setValue(key,val)

    def loadValue(self, key):
        return self.value(key, '')
    ########################################################################
    # ini file saves annoyingly long escape encodings on json
    def save(self, key, val):
        val = json.dumps(val)
        val = val.encode('utf-8')
        val = base64.encodebytes(val)
        val = str(val, 'ascii')
        self.setValue(key, val)

    def load(self, key, alt=''):
        val = self.value(key, None)
        if val is not None:
            val = val.encode('ascii')
            val = base64.decodebytes(val)
            val = val.decode('utf-8')
            return json.loads(val)
        return alt
