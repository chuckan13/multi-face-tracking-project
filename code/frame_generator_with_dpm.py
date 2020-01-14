"""
Generates frames and bounding boxes of frames using DPM
"""
import frame
import json
import cv2
import numpy as np
from shapely import geometry
# name of video = "westlife", etc.
# params is a dict of params

def generate_frames(name_of_video, source_of_frames, params):

    rows, cols, _ = cv2.imread(name_of_video + "_frames/" + name_of_video + "001.jpg").shape
    body_parts = {"chest": 1,
                  "left_shoulder": 2,
                  "left_elbow": 3,
                  "left_hand": 4,
                  "right_shoulder": 5,
                  "right_elbow": 6,
                  "right_hand": 7,
                  "pelvis": 8,
                  "left_hip": 9,
                  "left_knee": 10,
                  "left_ankle": 11,
                  "right_hip": 12,
                  "right_knee": 13,
                  "right_ankle": 14}

    body_part_pairs = [("chest", "pelvis"),
                       ("left_shoulder", "left_elbow"),
                       ("left_elbow", "left_hand"),
                       ("right_shoulder", "right_elbow"),
                       ("right_elbow", "right_hand"),
                       ("left_hip", "left_knee"),
                       ("left_knee", "left_ankle"),
                       ("right_hip", "right_knee"),
                       ("right_knee", "right_ankle")]

    frames = []
    for counter in range(1, params["frames"]+1):
        with open(name_of_video+"_keypoints_with_face/"+name_of_video+"_{0:0=12d}_keypoints.json".format(counter - 1)) as file:
            data = json.load(file)

        left = []
        right = []
        top = []
        bottom = []
        confidence = []
        polygons = []

        for list in data["people"]:
            keypoints = list["pose_keypoints_2d"] + list["face_keypoints_2d"]
            face_keypoints = list["face_keypoints_2d"]

            if getFaceConfidence(keypoints) > .80:
                # Face bounding box based on eye distance
                # eyea_x = keypoints[36 * 3] + keypoints[37 * 3] + keypoints[38 * 3] \
                #          + keypoints[39 * 3] + keypoints[40 * 3] + keypoints[41 * 3]
                # eyea_x = eyea_x / 6 * cols
                # eyea_y = keypoints[36 * 3 + 1] + keypoints[37 * 3 + 1] + keypoints[38 * 3 + 1] \
                #          + keypoints[39 * 3 + 1] + keypoints[40 * 3 + 1] + keypoints[41 * 3 + 1]
                # eyea_y = eyea_y / 6 * rows
                # eyeb_x = keypoints[42 * 3] + keypoints[43 * 3] + keypoints[44 * 3] \
                #          + keypoints[45 * 3] + keypoints[46 * 3] + keypoints[47 * 3]
                # eyeb_x = eyeb_x / 6 * cols
                # eyeb_y = keypoints[42 * 3 + 1] + keypoints[43 * 3 + 1] + keypoints[44 * 3 + 1] \
                #          + keypoints[45 * 3 + 1] + keypoints[46 * 3 + 1] + keypoints[47 * 3 + 1]
                # eyeb_y = eyeb_y / 6 * rows
                eyea_x = keypoints[15*3] * cols
                eyea_y = keypoints[15*3 + 1] * rows
                eyeb_x = keypoints[16*3] * cols
                eyeb_y = keypoints[16*3 + 1] * rows

                inter_eye_distance = eyeb_x - eyea_x
                if inter_eye_distance > 1:
                    x1 = int(eyea_x - (.55 * inter_eye_distance))
                    x2 = int(eyeb_x + (.55 * inter_eye_distance))
                    y1 = int(eyea_y + (1.45 * inter_eye_distance))
                    y2 = int(eyea_y - (1 * inter_eye_distance))

                    x1 = min(cols, x1)
                    x1 = max(0, x1)
                    x2 = min(cols, x2)
                    x2 = max(0, x2)
                    y1 = min(rows, y1)
                    y1 = max(0, y1)
                    y2 = min(rows, y2)
                    y2 = max(0, y2)

                    assert(x1!=x2)
                    assert(y1!=y2)

                    left.append(min(x1,x2))
                    right.append(max(x1,x2))
                    top.append(min(y1,y2))
                    bottom.append(max(y1,y2))
                    confidence.append(getFaceConfidence(keypoints))

                    # Create polygons
                    polygons_list = [None for x in range(len(body_part_pairs))]
                    for i in range(len(body_part_pairs)):
                        pair = body_part_pairs[i]
                        parta, partb = pair
                        aindex = body_parts[parta] * 3
                        bindex = body_parts[partb] * 3
                        x1 = int(keypoints[aindex] * cols)
                        y1 = int(keypoints[aindex + 1] * rows)
                        x2 = int(keypoints[bindex] * cols)
                        y2 = int(keypoints[bindex + 1] * rows)

                        if x1 != 0 and y2 != 0 and x1 != 0 and y2 != 0:
                            a = np.array((x1, y1))
                            b = np.array((x2, y2))
                            width = .4 * np.linalg.norm(a - b)
                            points = generateRectCoords(x1, y1, x2, y2, width, rows, cols)
                            polygons_list[i] = geometry.Polygon(points)
                    polygons.append(polygons_list)

        new_frame = frame.Frame(left, right, top, bottom, confidence, counter, polygons=polygons)
        frames.append(new_frame)

    return frames

def parse_line(line):
    return [line.split(" ")[3], line.split(" ")[5], line.split(" ")[7], line.split(" ")[9], line.split(" ")[11]]

def generateRectCoords(x1,y1,x2,y2,w, rows, cols):
    theta = np.arctan(y1/x1)

    xa = x1 + (w * np.sin(theta))
    ya = y1 + (w * np.cos(theta))
    xb = x1 - (w * np.sin(theta))
    yb = y1 - (w * np.cos(theta))
    xc = x2 + (w * np.sin(theta))
    yc = y2 + (w * np.cos(theta))
    xd = x2 - (w * np.sin(theta))
    yd = y2 - (w * np.cos(theta))

    xa = max(0, xa)
    xa = min(xa, cols)
    xb = max(0, xb)
    xb = min(xb, cols)
    xc = max(0, xc)
    xc = min(xc, cols)
    xd = max(0, xd)
    xd = min(xd, cols)

    ya = max(0, ya)
    ya = min(ya, rows)
    yb = max(0, yb)
    yb = min(yb, rows)
    yc = max(0, yc)
    yc = min(yc, rows)
    yd = max(0, yd)
    yd = min(yd, rows)

    return [(xa, ya), (xc, yc), (xd, yd) ,(xb, yb)]

# def getFaceConfidence(face_keypoints):
#     cumul_confidence = 0
#     for i in range (70):
#         index = i*3 + 2
#         cumul_confidence += face_keypoints[index]
#     return cumul_confidence/70


def getFaceConfidence(keypoints):
    return (keypoints[15*3 +2] + keypoints[16*3 + 2])/2