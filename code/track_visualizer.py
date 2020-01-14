"""
Visualizes the tracks by drawing bounding boxes and id onto original video.
Returns a video file containing bounding boxes and id.
"""
import cv2

class TrackVisualizer:

    def visualize(self, list_of_tracks, frames, output_path, video_name):
        # tracks_at_frame[i] is a list of tracks at frame i
        tracks_at_frame = self._build_tracks_at_frame(list_of_tracks, frames)

        rows, cols, _ = cv2.imread(video_name + "_frames/" + video_name+"001.jpg").shape

        image_list = []
        for counter in range(frames):
            image_list.append(cv2.imread(video_name + "_frames/" + video_name + "{0:0=3d}.jpg".format(counter), 1))


        for frame_num in range(frames):
            for track in tracks_at_frame[frame_num]:
                bounding_box_coords = track.getBoundingBoxAtFrame(frame_num)
                if bounding_box_coords != None:
                    a, b, c, d = bounding_box_coords
                    cv2.rectangle(image_list[frame_num], (a, c), (b, d), track.getColor(), 3)
                    id = "".join(str(x) for x in track.getColor())
                    cv2.putText(img=image_list[frame_num], text=id, org=(a,c),
                                fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=track.getColor(),
                                thickness=2)

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        video = cv2.VideoWriter(output_path, fourcc, 15, (cols, rows))
        for counter in range(frames):
            video.write(image_list[counter])

    def _build_tracks_at_frame(self, list_of_tracks, frames):
        tracks_at_frame = [[] for Null in range(frames+1)]

        for track in list_of_tracks:
            list_of_frames = track.getFrames()
            for frame_range in list_of_frames:
                init_frame, end_frame = frame_range
                for i in range(init_frame, end_frame+1):
                    tracks_at_frame[i].append(track)

        return tracks_at_frame