
'''
ItemController is an aggregate controller for dict-like objects.
When setting an item, all objects will receive the item
When getting an item, the first object is used as loadreference
The general idea:

    session = ItemController()
    session.add(fast_storage)
    session.add(slow_storage)

    pattern:
    if session[key] != value:  <-- fetched from fast_storage
        session[key] = value   <-- stuffed in all storages

'''

class ItemController:
    def __init__(self, ref=None):
        self._ref = ref
        self._dst = []

    def add(self, dst):
        if self._ref is None:
            self._ref = dst
        else:
            self._dst.append(dst)

    # Set item for all destination objects
    def __setitem__(self, key, val):
        self._ref[key] = val
        for dst in self._dst: dst[key] = val

    # Get item
    def __getitem__(self, key):
        return self.get(key)

    def get(self, key, alt=None):
        try: return self._ref[key]
        except KeyError: return alt

    def keys(self):
        if hasattr(self._ref, 'keys'):
            return self._ref.keys()
        return []

    def items(self):
        if hasattr(self._ref, 'items'):
            return self._ref.items()
        return []
