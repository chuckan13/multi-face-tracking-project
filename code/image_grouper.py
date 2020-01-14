"""
Generates high/low res groups. Applies k-means method to separate all tracklets based on the average
image size of each tracklet.
"""

import sklearn.cluster
import numpy as np

class ImageGrouper:

    def __init__(self, tracklets):
        tracklets_with_faces = []
        average_img_sizes = []
        for tracklet in tracklets:
            avg_img_size = self.get_average_image_size(tracklet)
            if avg_img_size != None:
                tracklets_with_faces.append(tracklet)
                average_img_sizes.append(avg_img_size)

        cluster_indeces = self.perform_k_means(average_img_sizes)

        group1 = []
        group2 = []
        for i in range(len(tracklets_with_faces)):
            if (cluster_indeces[i] == 0):
                group1.append(tracklets_with_faces[i])
            else:
                group2.append(tracklets_with_faces[i])

        self.determine_large_small(group1, group2)

    def determine_large_small(self, group1, group2):
        group1_img_size = 0
        for tracklet in group1:
            group1_img_size += self.get_average_image_size(tracklet)
        group1_img_size = group1_img_size / len(group1)
        group2_img_size = 0
        for tracklet in group2:
            group2_img_size += self.get_average_image_size(tracklet)
        group2_img_size = group2_img_size / len(group2)

        if (group2_img_size > group1_img_size):
            self.large_group = group2
            self.small_group = group1
        else:
            self.small_group = group2
            self.large_group = group1

    def perform_k_means(self, average_image_sizes):
        km = sklearn.cluster.KMeans(n_clusters=2)
        average_img_sizes = np.array(average_image_sizes)
        cluster_indeces = km.fit_predict(average_img_sizes.reshape(-1, 1))  # -1 will be calculated to be num_tracklets
        return cluster_indeces

    def get_average_image_size(self, tracklet):
        img_size_cumul = 0
        imgs_added = 0
        for coord in tracklet.bounding_boxes:
            if coord is not None:
                x_min, x_max, y_min, y_max = coord
                img_size = (y_max - y_min) * (x_max - x_min)
                img_size_cumul += img_size
                imgs_added += 1
        if imgs_added == 0:
            return None
        return img_size_cumul / imgs_added

    def get_large_images(self):
        return self.large_group

    def get_small_images(self):
        return self.small_group
