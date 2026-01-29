
import os

from qgis.core import QgsApplication

def qml_path(lang=None):
    lang = lang or QgsApplication.instance().locale()
    return _qml_path(lang) or _qml_path('en')

def _qml_path(lang):
    path = os.path.dirname(__file__)
    path = os.path.join(path, str(lang).lower()+'.qml')
    if os.path.exists(path): return path
