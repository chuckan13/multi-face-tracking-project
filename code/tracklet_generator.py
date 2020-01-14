"""
Generates tracklets.
"""
import tracklet


def gen_tracklets(frames, params):
    inactive_tracklets = []
    active_tracklets = []
    # Loop through all frames to build tracklets
    for frame in frames:
        new_active_tracklets = []
        indeces_inspected = []

        # First, we see which previous tracklets we can continue
        continue_tracklets(frame, active_tracklets, inactive_tracklets, new_active_tracklets, indeces_inspected, params)
        # Now, try to add new tracklets
        add_new_tracklets(frame, new_active_tracklets, indeces_inspected, params)

        active_tracklets = new_active_tracklets

    return inactive_tracklets+active_tracklets

def continue_tracklets(frame, active_tracklets, inactive_tracklets, new_active_tracklets, indeces_added, params):
    list_of_lefts = frame.list_of_lefts
    list_of_rights = frame.list_of_rights
    list_of_tops = frame.list_of_tops
    list_of_bottoms = frame.list_of_bottoms

    for tracklet in active_tracklets:
        max_overlap_index = 0
        max_overlap_value = 0

        for index in range(len(list_of_lefts)):
            if index not in indeces_added:
                overlap = tracklet.overlapWithLastBoundingBox([list_of_lefts[index],
                                                               list_of_rights[index],
                                                               list_of_tops[index],
                                                               list_of_bottoms[index]])
                if (overlap > max_overlap_value):
                    max_overlap_value = overlap
                    max_overlap_index = index

        if max_overlap_value > params["low_threshold"]:
            tracklet.addFrame([list_of_lefts[max_overlap_index],
                               list_of_rights[max_overlap_index],
                               list_of_tops[max_overlap_index],
                               list_of_bottoms[max_overlap_index]])
            new_active_tracklets.append(tracklet)
            indeces_added.append(max_overlap_index)

        else:
            inactive_tracklets.append(tracklet)

def add_new_tracklets(frame, new_active_tracklets, indeces_inspected, params):

    list_of_lefts = frame.list_of_lefts
    list_of_rights = frame.list_of_rights
    list_of_tops = frame.list_of_tops
    list_of_bottoms = frame.list_of_bottoms
    list_of_confidences = frame.list_of_confidences

    for index in range(len(list_of_lefts)):
        if index not in indeces_inspected:
            if list_of_confidences[index] > params["high_threshold"]:
                new_tracklet = tracklet.Tracklet(frame.frame_number,
                                                [list_of_lefts[index],
                                                 list_of_rights[index],
                                                 list_of_tops[index],
                                                 list_of_bottoms[index]])
                new_active_tracklets.append(new_tracklet)