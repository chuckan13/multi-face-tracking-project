"""
Tracklet object.
Tracklets contain Frames.
"""

import random

class Tracklet:

    # init_bounding_box in the form [left, right, top, bottom]
    def __init__(self, init_frame_number, init_bounding_box):
        self.first_frame = init_frame_number
        self.last_frame = init_frame_number
        self.bounding_boxes = [init_bounding_box]
        self.color = (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))
        self.id = "".join(str(x) for x in self.color)

    def getBoundingBoxes(self):
        return self.bounding_boxes

    def addFrame(self, bounding_box):
        self.last_frame += 1
        self.bounding_boxes.append(bounding_box)

    def isCoexisting(self, tracklet):
        start_current = self.first_frame
        end_current = self.last_frame
        start_other = tracklet.first_frame
        end_other = tracklet.last_frame
        return (start_current <= start_other <= end_current
                or start_current <= end_other <= end_current
                or start_other <= start_current <= end_other
                or start_other <= end_current <= end_other)

    def setFeatures(self, features):
        self.features = features

    def overlapWithLastBoundingBox(self, bounding_box):
        last_bounding_box = self.bounding_boxes[-1]

        lefta = bounding_box[0]
        righta = bounding_box[1]
        topa = bounding_box[2]
        bottoma = bounding_box[3]

        leftb = last_bounding_box[0]
        rightb = last_bounding_box[1]
        topb = last_bounding_box[2]
        bottomb = last_bounding_box[3]

        # 𝐴𝑜𝑣𝑒𝑟𝑙𝑎𝑝 = (max(𝑙0, 𝑙1)−min(𝑟0, 𝑟1))⋅(max(𝑡0, 𝑡1)−min(𝑏0, 𝑏1)).
        width = (min(righta, rightb) - max(lefta, leftb))
        height = (min(bottoma, bottomb) - max(topa, topb))

        # no overlap
        if width < 0 or height < 0:
            return 0

        overlap = width*height
        areaa = (righta-lefta) * (bottoma-topa)
        areab = (rightb-leftb) * (bottomb-topb)

        return overlap/(areaa + areab - overlap)




