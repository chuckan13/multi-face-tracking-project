"""
Calculates Weighted Cluster Purity score.
"""

import frame_generator
import tracklet_generator
import tracklet_visualizer
import tracklet_face_saver
import image_grouper
import keypoints_extractor
import link_builder
import track_visualizer
import track_saver
import tracklet_saver
import clear_mot
from clear_mot import parseXML
import motmetrics as mm
import numpy as np

tracks = track_saver.readTracks()
ground_truth, list_of_trajectories = parseXML("GT/GirlsAloud_gt.xml", 2970)

for track in tracks:
    list_of_indexes = [None]*2971
    list_of_frames = track.getFrames()

    for frame_range in list_of_frames:
        init_frame, end_frame = frame_range
        for i in range(init_frame, end_frame+1):
            bounding_boxes = track.getBoundingBoxAtFrame(i)
            width = bounding_boxes[1]-bounding_boxes[0]
            height = bounding_boxes[3]-bounding_boxes[2]
            bounding_boxes[1]=bounding_boxes[2]
            bounding_boxes[2]=width
            bounding_boxes[3]=height

            dist_array = mm.distances.iou_matrix(ground_truth[i], np.array([bounding_boxes]), max_iou=0.5)
 
            if len(dist_array)>0:
                min_dist = dist_array[0][0]
                min_index = list_of_trajectories[i][0]
                for j in range(len(dist_array)):
                    if dist_array[j][0] < min_dist:
                        min_dist = dist_array[j][0]
                        min_index = list_of_trajectories[i][j]

                list_of_indexes[i]=min_index

    track.setListOfIndexes(list_of_indexes)
                
total_faces_detected = 0
sum_of_max_faces_from_same_person = 0
for track in tracks:
    list_of_indexes = track.list_of_indexes
    list_of_frames = track.getFrames()
    faces_from_same_person = [0,0,0,0,0,0]
    max_faces_from_same_person=0

    for frame_range in list_of_frames:
        init_frame, end_frame = frame_range
        for i in range(init_frame, end_frame+1):
            if list_of_indexes[i] is not None:
                faces_from_same_person[int(list_of_indexes[i])-1] += 1
    
    total_faces_detected += sum(faces_from_same_person)
    max_faces_from_same_person = max(faces_from_same_person)
    sum_of_max_faces_from_same_person += max_faces_from_same_person

wcp_score = sum_of_max_faces_from_same_person / total_faces_detected

print("WCP Score: ", wcp_score)
