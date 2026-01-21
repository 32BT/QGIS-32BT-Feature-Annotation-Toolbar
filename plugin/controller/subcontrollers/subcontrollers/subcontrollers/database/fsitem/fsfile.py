
from .fsitem import FSItem

################################################################################

class FSFile(FSItem):

    @classmethod
    def validate_path(cls, path):
        return FSItem.path_isfile(path)


    def open(self, mode='r', encoding='utf-8'):
        return open(self._path, mode, encoding=encoding)

    def read(self, mode='r', encoding='utf-8'):
        with self.open(mode, encoding) as f: return f.read()

    def remove(self):
        if self.exists():
            os.remove(self._path)
            return True
        return False

    ########################################################################

    def writeText(self, txt, mode='w'):
        with self.open(mode) as f: f.write(txt)

    def appendText(self, txt):
        self.writeText(txt, 'a')

    def appendLine(self, txt, eolc='\n'):
        self.writeText(txt+eolc, 'a')

    ########################################################################

    def readText(self, alt=None):
        try:
            return self.read()
        except Exception:
            return alt

    def readLine(self, idx=0):
        with self.open() as f:
            for _ in range(idx): next(f)
            return next(f).strip()

    def __iter__(self):
        try:
            with self.open() as f:
                return iter(list(f))
        except Exception:
            return iter([])
################################################################################
