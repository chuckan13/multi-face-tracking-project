"""
Saves tracklets to a local directory.
"""
import pickle
import os

def saveTracklets(large_group, small_group):
    # Delete all files in directory
    filelist = [f for f in os.listdir("saved_tracklets_large")]
    for f in filelist:
        os.remove(os.path.join("saved_tracklets_large", f))
    filelist = [f for f in os.listdir("saved_tracklets_small")]
    for f in filelist:
        os.remove(os.path.join("saved_tracklets_small", f))

    counter = 0
    for tracklet in large_group:
        file = open("saved_tracklets_large/"+str(counter)+".obj", 'wb')
        pickle.dump(tracklet, file)
        counter+=1
    counter = 0
    for tracklet in small_group:
        file = open("saved_tracklets_small/"+str(counter)+".obj", 'wb')
        pickle.dump(tracklet, file)
        counter+=1

def readTracklets():
    small_tracklets = []
    for filename in os.listdir("saved_tracklets_small"):
        file = open("saved_tracklets_small/"+filename, 'rb')
        small_tracklets.append(pickle.load(file))
    large_tracklets = []
    for filename in os.listdir("saved_tracklets_large"):
        file = open("saved_tracklets_large/" + filename, 'rb')
        large_tracklets.append(pickle.load(file))

    return small_tracklets, large_tracklets