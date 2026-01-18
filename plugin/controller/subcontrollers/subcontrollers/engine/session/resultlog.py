

from ..database import LOGFile


class ResultLog(LOGFile):
    def __setitem__(self, guid, result):
        date = self.get_date()
        user = self.get_user()
        super().__setitem__(date, (user, result, guid))
