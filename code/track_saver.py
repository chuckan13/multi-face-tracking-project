"""
Saves tracks to local directory.
"""

import pickle
import os

def saveTracks(tracks_list):
    # Delete everythin in dir
    filelist = [f for f in os.listdir("saved_tracks")]
    for f in filelist:
        os.remove(os.path.join("saved_tracks", f))

    counter = 0
    for track in tracks_list:
        file = open("saved_tracks/"+str(counter)+".obj", 'wb')
        pickle.dump(track, file)
        counter+=1

def readTracks():
    tracks = []
    for filename in os.listdir("saved_tracks"):
        file = open("saved_tracks/"+filename, 'rb')
        tracks.append(pickle.load(file))

    return tracks