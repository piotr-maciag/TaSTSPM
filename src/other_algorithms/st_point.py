class STPoint:
    def __init__(self, eventID, eventType, spatialX, spatialY, temporal):
        self.eventID = eventID
        self.eventType = eventType
        self.spatialX = spatialX
        self.spatialY = spatialY
        self.temporal = temporal


    def __repr__(self):
        return f"STPoint(eventID={self.eventID}, eventType='{self.eventType}', spatialX={self.spatialX}, spatialY={self.spatialY}, temporal={self.temporal})"