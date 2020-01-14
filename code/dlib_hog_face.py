"""
Detects faces using Dlib's HOG face detector.
Returns text files with coordinates of bounding boxes.
Code adapted from Dlib's example code: http://dlib.net/
"""

import sys
import os
import dlib

detector = dlib.get_frontal_face_detector()

for f in sys.argv[1:]:
    print("Processing file: {}".format(f))
    img = dlib.load_rgb_image(f)
    # The 1 in the second argument indicates that we should upsample the image
    # 1 time.  This will make everything bigger and allow us to detect more
    # faces.
    dets = detector(img, 1)
    print("Number of faces detected: {}".format(len(dets)))
    file_name = os.path.splitext(f)[0]+".txt"
    file_name = os.path.split(file_name)[0]+"/keypoints_hog/"+os.path.split(file_name)[1]
    f = open(file_name, "w")
    for i, d in enumerate(dets):
        print("Detection {}: Left: {} Top: {} Right: {} Bottom: {} Confidence: 1.0".format(
            i, d.left(), d.top(), d.right(), d.bottom()))
        f.write("Detection {}: Left: {} Top: {} Right: {} Bottom: {} Confidence: 1.0".format(
            i, d.left(), d.top(), d.right(), d.bottom()))
        f.write("\n")
        print("written to"+file_name)
    f.close()

# Finally, if you really want to you can ask the detector to tell you the score
# for each detection.  The score is bigger for more confident detections.
# The third argument to run is an optional adjustment to the detection threshold,
# where a negative value will return more detections and a positive value fewer.
# Also, the idx tells you which of the face sub-detectors matched.  This can be
# used to broadly identify faces in different orientations.
if (len(sys.argv[1:]) > 0):
    img = dlib.load_rgb_image(sys.argv[1])
    dets, scores, idx = detector.run(img, 1, -1)
    for i, d in enumerate(dets):
        print("Detection {}, score: {}, face_type:{}".format(
            d, scores[i], idx[i]))
