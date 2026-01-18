

from ..database import CSVFile


################################################################################
### ResultFile
################################################################################
'''
ResultFile is a CSVFile for (guid,result) combos with a cache dict.
The cache dictionary is used to test for existing entries, and for
rewriting the file in case a result is replaced.

ResultFile is a CSVFile. Use start(hdr) at some point to write the header and
start the file.

Note that ResultFile can also be designed as an ItemController:
    ItemController
        add(dict)     <-- fastest storage first
        add(CSVFile)

    where dict can be instantiated using dict(CSVFile.readRows())

    ItemController.get will get from dict
    ItemController.set will set both containers

    Tricky part: refresh csv


'''

class ResultFile(CSVFile):

    ########################################################################

    def cache(self):
        if not hasattr(self, '_cache'):
            self._cache = dict(self.readRows())
        return self._cache

    def keys(self):
        return self.cache().keys()

    def items(self):
        return self.cache().items()

    def __getitem__(self, guid):
        return self.get(guid)

    def __setitem__(self, guid, label):
        self.set(guid, label)

    ########################################################################

    def get(self, guid, alt=None):
        return self.cache().get(guid, alt)

    '''
    ResultFile.set(...) stores a guid/result combo in its cache and in its file.
    It can be considered the absolute core of processing. It also makes it
    the quickest way to test for actual change.
    If this returns True, then all other representations should also update.
    '''
    def set(self, guid, result):
        data = self.cache()
        if data.get(guid) != result:
            size = len(data)
            data[guid] = result
            if len(data) == size:
                self.refresh()
            else:
                self.appendValues(guid, result)
            return True
        return False

    ########################################################################
    '''
    A CSVFile can only append entries. If the result for an existing entry is
    changed, then the file must be rewritten from scratch. Note that cache
    will exist at this point since that is how we check for existing entries.

    TODO safesave
    '''
    def refresh(self):
        # Rewrite header will restart file
        self.start(*self.readHdr())
        # Append all items from cache
        for k,v in self._cache.items():
            self.appendValues(k,v)

    ########################################################################
