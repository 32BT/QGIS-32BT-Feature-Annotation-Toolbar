

from qgis.gui import *
from qgis.PyQt.QtCore import *


################################################################################
### Marker MapTool
################################################################################
'''
QgsMapToolEmitPoint responds to mousedown, not mouseup.
If we place a marker, we generally would want it placed at the location where
we release the mousebutton. In addition, if we want to reset our tool on
canvasClicked, we should not use mousedown, because a subsequent mouseup event
will then be transmitted to the new tool.
'''
class MarkerMapTool(QgsMapToolEmitPoint):
    canvasUnclicked = pyqtSignal(object, object)

    def canvasReleaseEvent(self, event):
        p = self.toMapCoordinates(event.pos())
        self.canvasUnclicked.emit(p, event.button())

################################################################################
### Marker MapTool with panning
################################################################################

class PanningMarkerMapTool(MarkerMapTool):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.resetTracking()
        self.tolerance = 5

    def activate(self):
        super().activate()
        self.resetTracking()

    def resetTracking(self):
        self._tracking = False
        self._position = None

    def canvasPressEvent(self, event):
        self._tracking = False
        self._position = event.pos()

    def canvasMoveEvent(self, event):
        if self._tracking:
            self.canvas().panAction(event)
        elif self._position is not None:
            dx = abs(self._position.x()-event.pos().x())
            dy = abs(self._position.y()-event.pos().y())
            self._tracking = (dx*dx+dy*dy)>(self.tolerance*self.tolerance)

    def canvasReleaseEvent(self, event):
        if self._tracking:
            self.canvas().panActionEnd(event.pos())
        else:
            mapLocation = self.toMapCoordinates(self._position)
            self.canvasClicked.emit(mapLocation, event.button())
        self.resetTracking()
