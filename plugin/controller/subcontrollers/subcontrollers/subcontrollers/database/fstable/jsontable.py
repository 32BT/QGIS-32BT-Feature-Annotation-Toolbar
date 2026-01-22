
################################################################################
### JSONTable
################################################################################

import json
from .fstable import FSTable

class JSONTable(FSTable):
    ITEM_EXT = '.json'

    def start(self, itemClass=None):
        self.ITEM_CLS=itemClass
        return super().start()

    def saveTableItem(self, guid, item):
        text = self.item_as_json(item)
        if text: return super().saveTableItem(guid, text)

    def loadTableItem(self, guid):
        text = super().loadTableItem(guid)
        if text: return self.item_from_json(text)

    ########################################################################

    def item_as_json(self, item):
        try: return item.as_json()
        except AttributeError: pass
        try: return json.dumps(item)
        except Exception: pass

    def item_from_json(self, text):
        try: return self.ITEM_CLS.from_json(text)
        except AttributeError: pass
        try: return json.loads(text)
        except Exception: pass

    ########################################################################
