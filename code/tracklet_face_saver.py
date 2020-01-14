"""
Saves faces in tracklets into local directory.
"""
import shutil
import os
import cv2

def save(tracklets, output_folder, video_name):
    # delete output folder that currently exists
    shutil.rmtree(output_folder, ignore_errors=True)
    os.mkdir(output_folder)
    print("Saving faces...")

    for tracklet in tracklets:
        first_frame = tracklet.first_frame
        last_frame = tracklet.last_frame

        image_list = []
        for i in range(first_frame, last_frame + 1):
            image_list.append(cv2.imread(video_name+"_frames/"+video_name+"{0:0=3d}.jpg".format(i), 1))

        bounding_boxes = tracklet.bounding_boxes

        for i in range(last_frame - first_frame + 1):
            # Write images
            if (bounding_boxes[i] != None):
                left, right, top, bottom = bounding_boxes[i]
                face = image_list[i][top:bottom, left:right]

                assert (left < right)
                assert (top < bottom)
                assert (left >= 0)
                assert (right >= 0)
                assert (top >= 0)
                assert (bottom >= 0)

                folder = "/{}".format(tracklet.id)
                file = "/{}.jpg".format(i)
                if not os.path.exists(output_folder + folder):
                    os.mkdir(output_folder + folder)
                cv2.imwrite(output_folder + folder + file, face)



