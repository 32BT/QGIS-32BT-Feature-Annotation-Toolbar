
import os

from .. import FSFolder, FSFile

class Item(FSFolder):

    def start(self, value):
        super().start()
        if isinstance(value, dict):
            for k,v in value.items():
                self[k] = v
        if isinstance(value, list):
            for i, v in enumerate(value):
                self[i] = v

    def __setitem__(self, key, value):
        path = self.itemPath(str(key))
        if (isinstance(value, dict) or
            isinstance(value, list)):
            self.__class__(path).start(value)
        else:
            FSFile(path+'.txt').writeText(str(value))


'''
{
   "type": "FeatureCollection",
   "name": "Example Feature Collection"
   "itemCount": 0
   "items": {
        <name 0>: <feature 0>,
        <name 1>: <feature 1>,
        ...
   }
}

{
    "type": "Feature",
    "name": id_as_str
    "itemCount": 2
    "items": {
        "path": []
        "prop0": <value0> }
}


{
    "type": "crs"
    "name": "urn:..."
}

{
    "type": "Feature",
    "name": id_as_str
    "geometry": {
        "type": "Path", "Point", "LineString", "Polygon"
        "coordinates": [102.0, 0.5]
        "coordinateCount": number of coordinates
        "dimensions": ["X", "Y", "Z", "M", ...]
        "path": [102.0, 0.5]
    },
    "properties": {
        "prop0": "value0"
    }
}






path
array similar to svg "d"

If first coordinate is not preceded by a command character,
then it will be interpreted as an absolute moveto or "M".

A path with only a single coordinate and no command characters, is a point.

path and multitype?


'''
