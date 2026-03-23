

import os

from .fsfile import FSFile

class CSVFile(FSFile):
    DEFAULT_EXT = '.csv'
    DEFAULT_EOL = '\n'

    @classmethod
    def validateName(cls, name):
        return os.path.splitext(name)[-1].lower() == cls.DEFAULT_EXT


    def __init__(self, path, name=None):
        super().__init__(path, name)
        self._eol = self.DEFAULT_EOL
        self._hdr = None

    def appendLine(self, txt):
        if txt: super().appendLine(txt, self._eol)

    '''
    start is used to start a CSVFile by writing its header.
    It returns self as a convenience.
    '''
    def start(self, *hdr):
        self._hdr = hdr
        self.writeText('')
        self.appendLine(self._merge(hdr))
        return self

    '''
    Fetch columnName at index, or return None
    '''
    def columnName(self, idx):
        hdr = self.readHdr()
        if hdr and 0<=idx<len(hdr):
            return hdr[idx]

    ########################################################################
    ### Item Control
    ########################################################################
    '''
    '''
    def __setitem__(self, rowid, data):
        if not isinstance(data, tuple): data = (data,)
        #self.appendValues([rowid]+list(data))
        self.appendValues(rowid, *data)

    def __getitem__(self, rowid):
        rows = list(self.findRows(rowid))
        if rows:
            row = rows[-1]
            if len(row) == 1: return row[0]
            if len(row) == 2: return row[1]
            return row[1:]

    def findRows(self, rowid):
        for row in self.readRows():
            if row[0] == rowid: yield row

    ########################################################################
    ### Save
    ########################################################################

    def appendItems(self, items):
        if not self.exists() and items:
            self.appendValues(items[0].keys())
        for item in items:
            self.appendValues(item.values())

    def appendItem(self, item):
        if not self.exists():
            self.appendValues(item.keys())
        self.appendValues(item.values())

    def appendValues(self, *values):
        self.appendLine(self._merge(*values))

    def _merge(self, *values):
        if len(values)==1: values = values[0]
        txt = (str(v).strip() for v in values)
        txt = ','.join(txt)
        return txt

    ########################################################################
    ### Load
    ########################################################################
    def __iter__(self):
        return self.readItems()

    def readItems(self):
        hdr = self.readHdr()
        for row in self.readRows():
            yield(dict(zip(hdr, row)))

    def readHdr(self):
        try:
            with self.open() as f:
                return self._split(next(f))
        except Exception:
            pass

    def readRows(self, skip=1):
        try:
            with self.open() as f:
                for row in range(skip): next(f)
                for row in f: yield self._split(row)
        except Exception:
            pass

    def _split(self, row):
        return [w.strip() for w in row.split(',')]
