"""
Main file
To run: python main.py
Adjust params as needed.
"""
import frame_generator
import frame_generator_with_dpm
import frame_generator_with_mtcnn
import tracklet_generator
import tracklet_visualizer
import tracklet_face_saver
import image_grouper
import keypoints_extractor
import link_builder
import track_visualizer
import track_saver
import tracklet_saver
import frame_saver
import clear_mot
import wcp_score


params = {
    "frames" : 2500,
    "high_threshold" : .50,
    "low_threshold" : .10,
    "lt_threshold": .45,
    "lc_invalid_set_threshold": .65,
    "use_dpm" : True,
    "use_mtcnn": False,
    "video" : "westlife",
    "gt_file": "GT/Westlife_gt.xml"
}

def buildFrames():
    if params["use_dpm"]:
        frames = frame_generator_with_dpm.generate_frames(params["video"], "cnn", params)
    elif params["use_mtcnn"]:
        frames = frame_generator_with_mtcnn.generate_frames(params["video"], "cnn", params)
    else:
        frames = frame_generator.generate_frames(params["video"], "cnn", params)

    # Save frames
    frame_saver.saveFrames(frames)

def buildTracklets():
    # Load frames
    frames = frame_saver.readFrames()

    # Build tracklets from frames
    tracklets = tracklet_generator.gen_tracklets(frames, params)
    tracklet_visualizer.makeVideo(tracklets, params["frames"], params["video"], "output.mp4")
    tracklet_face_saver.save(tracklets, "tracklet_faces", params["video"])

    # Generate high/low res groups
    groups = image_grouper.ImageGrouper(tracklets)
    small_group = groups.get_small_images()
    large_group = groups.get_large_images()
    print(len(small_group+large_group)," Tracklets With Faces Found")
    print(len(small_group )," Tracklets in Small Cluster")
    print(len(large_group )," Tracklets in Large Cluster")

    # For each tracklet in large group, associate it with vgg-features
    extractor = keypoints_extractor.KeypointExtractor()
    print("Getting features...")
    counter = 0
    for tracklet in small_group + large_group:
        print(counter + 1, "/", len(small_group + large_group))
        tracklet.setFeatures(extractor.getAllFeatures(tracklet, "tracklet_faces"))
        counter += 1

    # Save tracklets
    tracklet_saver.saveTracklets(large_group, small_group)

def buildTracks():
    # Load tracklets
    small_group, large_group = tracklet_saver.readTracklets()

    # Build links and get full tracks
    print("Building links...")
    builder = link_builder.LinkBuilder(large_group, small_group, params)
    tracks = builder.build_links()
    builder.draw_graph()

    # Save tracks
    track_saver.saveTracks(tracks)

def runWithTracks():
    # Get tracks
    tracks = track_saver.readTracks()

    # Display video with tracks
    tvisualizer = track_visualizer.TrackVisualizer()
    tvisualizer.visualize(tracks, params["frames"], "track_vid.mp4", params["video"])

    # Display results
    print(clear_mot.getMetrics(tracks, params, params["gt_file"]))
    print(wcp_score.getWCP(tracks, params["gt_file"], params["frames"]))

buildFrames()
buildTracklets()
buildTracks()
runWithTracks()
