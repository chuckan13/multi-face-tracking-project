"""
Frame object that keeps track of the bounding boxes in the frame.
"""
class Frame:

    # any list is a list of integers representing the left/right/top/bottom coordinate of a bounding box
    # i.e bounding box 6 has bounding values list_of_lefts[5], list_of_rights[5], etc.
    def __init__(self, list_of_lefts, list_of_rights, list_of_tops, list_of_bottoms, list_of_confidences, frame_number):
        self.list_of_lefts = list_of_lefts
        self.list_of_rights = list_of_rights
        self.list_of_tops = list_of_tops
        self.list_of_bottoms = list_of_bottoms
        self.list_of_confidences = list_of_confidences
        self.frame_number = frame_number


