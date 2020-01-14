"""
Track object. 
Tracks contain tracklets.
"""

import random

class Track:

    def __init__(self, list_of_tracklets):
        self.color = (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))
        self.framesDict = {}
        self.list_of_tracklets = list_of_tracklets
        for tracklet in list_of_tracklets:
            color_id = "".join(str(x) for x in tracklet.color)
            frames = (tracklet.first_frame, tracklet.last_frame)
            self.framesDict[color_id] = frames

    def setListOfIndexes(self, list_of_indexes):
        self.list_of_indexes = list_of_indexes

    def getColor(self):
        return self.color

    def getFrames(self):
        return list(self.framesDict.values())

    def getTrackletIds(self):
        return list(self.framesDict.keys())

    def getFramesDict(self):
        return self.framesDict

    def getBoundingBoxAtFrame(self, frame):
        tracklet_at_frame = None
        for tracklet in self.list_of_tracklets:
            if tracklet.first_frame <= frame <= tracklet.last_frame:
                tracklet_at_frame = tracklet
                break
        assert(tracklet_at_frame != None)

        bounding_box_index = frame - tracklet.first_frame
        return tracklet.bounding_boxes[bounding_box_index]

