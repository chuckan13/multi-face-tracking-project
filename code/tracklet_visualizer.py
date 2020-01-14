"""
Visualizes the tracklets by drawing bounding boxes around the original video.
Saves to local directory.
"""
import cv2
import os
import shutil


def makeVideo (tracklets, num_frames, name_of_video, output_path):
    print("Saving video...")

    image_list = []
    tracklets = tracklets
    rows, cols, _ = cv2.imread(name_of_video+"_frames/"+ name_of_video +"001.jpg").shape

    for counter in range(num_frames):
        image_list.append(cv2.imread(name_of_video+"_frames/"+name_of_video+"{0:0=3d}.jpg".format(counter + 1), 1))

    for tracklet in tracklets:
        first_frame = tracklet.first_frame
        last_frame = tracklet.last_frame

        bounding_boxes = tracklet.bounding_boxes

        frame_num = first_frame
        while frame_num <= last_frame:
            # Draw face bounding boxes
            if (bounding_boxes[frame_num-first_frame] != None):
                a,b,c,d = bounding_boxes[frame_num-first_frame]
                cv2.rectangle(image_list[frame_num-1], (a,c), (b,d), tracklet.color)

            frame_num += 1
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video = cv2.VideoWriter(output_path, fourcc, 30, (cols, rows))
    for counter in range(num_frames):
        video.write(image_list[counter])

