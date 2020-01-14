"""
Calculates CLEAR MOT metrics, a benchmark for multiple object trackers
Uses py-motmetrics: github.com/cheind/py-motmetrics
"""

import motmetrics as mm
import numpy as np
from tabulate import tabulate
import xml.etree.ElementTree as ET 
import track_saver
import track_visualizer


# computes distances between frame objects and hypotheses
def compute_distance_matrix(gt, hypothesis):
    return mm.distances.iou_matrix(gt, hypothesis, max_iou=0.9) 

def generate_results(acc):
    metrics_array = ['recall', 'precision', 'idf1', 'num_false_positives', 'num_frames', 'mostly_tracked', 'num_switches', 'num_fragmentations', 'mota', 'motp']
    mh = mm.metrics.create()
    results = mh.compute(acc, metrics=metrics_array, name='acc')
    return results

def getResultsAsString(results):
    recall = results.recall.values[0]
    precision = results.precision.values[0]
    f1 = results.idf1.values[0]
    faf = results.num_false_positives.values[0] / results.num_frames.values[0]
    mt = results.mostly_tracked.values[0]
    ids = results.num_switches.values[0] 
    frag = results.num_fragmentations.values[0]
    mota = results.mota.values[0]
    motp = results.motp.values[0]
    metrics_array = ['Recall', 'Precision', 'F1', 'FAF', 'MT', 'IDS', 'Frag', 'MOTA', 'MOTP']
    values_array = [recall, precision, f1, faf, mt, ids, frag, mota, motp]
    result = str(tabulate([values_array], headers=metrics_array, tablefmt='orgtbl'))
    return result
    
def update_accumulator(acc, gt, hypothesis, list_of_trajectories, list_of_tracks, num_frames): # loop over each frame
    #call update once per frame
    for i in range(num_frames):
        dist_array = compute_distance_matrix(gt[i], hypothesis[i])
        if i==100:
            continue
        acc.update(
            list_of_trajectories[i], # ground truth objects in this frame
            list_of_tracks[i], # detector hypothesis in this frame
            dist_array
        )

    return acc

def build_tracks_at_frame(list_of_tracks, frames):
        tracks_at_frame = [[] for Null in range(frames+1)]
        hypothesis = [np.empty((0,4), int) for Null in range(frames+1)]

        for track in list_of_tracks:
            list_of_frames = track.getFrames()
            for frame_range in list_of_frames:
                init_frame, end_frame = frame_range
                for i in range(init_frame, end_frame+1):
                    tracks_at_frame[i].append("".join(str(x) for x in track.getColor()))

                    # left right top bottom
                    bounding_boxes = track.getBoundingBoxAtFrame(i)
                    width = bounding_boxes[1]-bounding_boxes[0]
                    height = bounding_boxes[3]-bounding_boxes[2]
                    bounding_boxes[1]=bounding_boxes[2]
                    bounding_boxes[2]=width
                    bounding_boxes[3]=height
                    hypothesis[i] = np.append(hypothesis[i], np.array([bounding_boxes]), axis=0)

        return tracks_at_frame, hypothesis

def parseXML(xmlfile, num_frames):
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    
    trajectories = [np.empty((0,4), int) for Null in range(num_frames+1)]
    list_of_trajectories = [[] for Null in range(num_frames+1)]

    for item in root:
        for children in item:         
            if int(children.attrib['frame_no']) <= num_frames:
                list_of_trajectories[int(children.attrib['frame_no'])].append(item.attrib['obj_id'])

                frame = []
                frame.append(int(children.attrib['x']))
                frame.append(int(children.attrib['y']))
                frame.append(int(children.attrib['width']))
                frame.append(int(children.attrib['height']))
                trajectories[int(children.attrib['frame_no'])] = np.append(trajectories[int(children.attrib['frame_no'])], np.array([frame]), axis=0)

    return trajectories, list_of_trajectories

def getMetrics(tracks, params, gt_file):
    num_frames = params["frames"]

    ground_truth, list_of_trajectories = parseXML(gt_file, num_frames)
    list_of_tracks, hypothesis = build_tracks_at_frame(tracks, num_frames)

    acc = mm.MOTAccumulator(auto_id=True)
    acc = update_accumulator(acc, ground_truth, hypothesis, list_of_trajectories, list_of_tracks, num_frames)
    results = generate_results(acc)
    return getResultsAsString(results)
