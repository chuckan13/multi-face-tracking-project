"""
Uses MTCNN to detect faces in frames
"""

# face detection with mtcnn on a photograph
from matplotlib import pyplot
from mtcnn.mtcnn import MTCNN
import frame
import cv2
# name of video = "westlife", etc.
# params is a dict of params

def generate_frames(name_of_video, source_of_frames, params):
    frames = []
    for counter in range(1, params["frames"]+1):
        print("Frame",counter, "/",params["frames"])

        left = []
        right = []
        top = []
        bottom = []
        confidence = []

        image = pyplot.imread(name_of_video + "_frames/" + name_of_video + "{0:0=3d}.jpg".format(counter))

        detector = MTCNN()
        faces = detector.detect_faces(image)
        for face in faces:
            l, t, w, h = face['box']
            r = l+w
            b = t+h
            left.append(l)
            right.append(r)
            top.append(t)
            bottom.append(b)
            confidence.append(face['confidence'])
        new_frame = frame.Frame(left, right, top, bottom, confidence, counter)
        frames.append(new_frame)

    return frames











