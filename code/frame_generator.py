"""
Generates Frame objects for the invidivual frames in source_of_frames
"""
import frame
# name of video = "westlife", etc.
# params is a dict of params

def generate_frames(name_of_video, source_of_frames, params):
    frames = []
    for counter in range(1, params["frames"]+1):
        with open(name_of_video+"_face_bounds_"+source_of_frames+"/"+name_of_video+"{0:0=3d}.txt".format(counter)) as file:
            left = []
            right = []
            top = []
            bottom = []
            confidence = []

            line = file.readline()
            while line:
                box = parse_line(line)

                if int(box[0])<0:
                    box[0] = 0
                if int(box[1])<0:
                    box[1] = 0

                left.append(int(box[0]))
                right.append(int(box[2]))
                top.append(int(box[1]))
                bottom.append(int(box[3]))

                confidence.append(float(box[4]))

                line = file.readline()


            new_frame = frame.Frame(left, right, top, bottom, confidence, counter)
            frames.append(new_frame)

    return frames


def parse_line(line):
    return [line.split(" ")[3], line.split(" ")[5], line.split(" ")[7], line.split(" ")[9], line.split(" ")[11]]