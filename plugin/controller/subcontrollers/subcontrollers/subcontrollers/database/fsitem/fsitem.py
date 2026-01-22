
import os, time

################################################################################
### Utilities
################################################################################
'''
fsitem utilities for consistency and readability.
'''
def path_exists(path):
    if path is not None:
        return os.path.exists(path)

def path_isfile(path):
    if path_exists(path):
        return os.path.isfile(path)

def path_isdir(path):
    if path_exists(path):
        return os.path.isdir(path)

def path_shrinkuser(path):
    home = os.path.expanduser('~')
    if home and path.startswith(home):
        path = '~'+path[len(home):]
    return path

def path_expanduser(path):
    return os.path.expanduser(path)

def path_parentpath(path):
    # Do not use os.path.dirname since it's an extremely confusing misnomer
    return os.path.split(path)[0]


################################################################################
### FSItem
################################################################################
'''
FSItem is a baseclass wrapping utilities for file-system manipulation.
Classhierarchy:

           FSFolder
          /
    FSItem
          \
           FSFile -> CSVFile -> LOGFile

'''

class FSItem:
    ########################################################################
    ### Namespace Utilities
    ########################################################################
    '''
    Classmethods should not interfere with instance methods.
    Naming pattern is meant to mimic instantiation order, e.g.:
        FSItem.path_parentpath(<path>)
        FSItem(<path>).parentPath()

    '''
    @classmethod
    def path_exists(cls, path):
        return path_exists(path)

    @classmethod
    def path_isfile(cls, path):
        return path_isfile(path)

    @classmethod
    def path_isdirectory(cls, path):
        return path_isdir(path)

    @classmethod
    def path_shrinkuser(cls, path):
        return path_shrinkuser(path)

    @classmethod
    def path_expanduser(cls, path):
        return path_expanduser(path)

    @classmethod
    def path_parentpath(cls, path):
        return path_parentpath(path)

    ########################################################################

    def __init__(self, path, name=None):
        if not name:
            path, name = os.path.split(path)
        self._name = name
        self._path = os.path.join(path, name)
        self._path = self.path_expanduser(self._path)

    def __str__(self):
        return self.path_shrinkuser(self._path)

    def name(self):
        return self._name

    def path(self):
        return self._path

    def exists(self):
        return self.path_exists(self._path)

    def isFile(self):
        return self.path_isfile(self._path)

    def isDirectory(self):
        return self.path_isdirectory(self._path)

    def parentPath(self):
        return self.path_parentpath(self._path)

    def shrinkPath(self):
        return self.path_shrinkuser(self._path)

    def chopPath(self, path):
        return os.path.relpath(path, self._path)

    def joinPath(self, path):
        return os.path.join(self._path, path)

    def splitExtension(self):
        return os.path.splitext(self._path)

    def parent(self):
        return self.__class__(self.parentPath())

    def rename(self, name):
        item = self.__class__(self.parentPath(), name)
        if self.exists():
            os.rename(self.path(), item.path())
        return item

    def moveTo(self, path, replace=False):
        if self.exists():
            move = os.replace if replace else os.rename
            try:
                move(self.path(), path)
                return self.__class__(path)
            except Exception as error:
                print(error)

################################################################################
### Temporary backup
################################################################################

class replace:
    def __init__(self, item):
        self._item = item.rename(item.name()+'.bck')

    def __enter__(self):
        return self

    def __exit__(self, *args):
        if args[0] is None:
            self._item.remove()
