"""
Builds {lt} and {lc} links
"""
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import track

class LinkBuilder:

    # Tracklets in large_group and small_group must have vgg-features associated!!
    def __init__(self, large_group, small_group, params):
        self.large_group = large_group
        self.small_group = small_group
        self.graph = nx.Graph()
        self.params = params

        # Add all tracklets as nodes in graph
        for tracklet in large_group:
            self.graph.add_node(tracklet)
        for tracklet in small_group:
            self.graph.add_node(tracklet)

    def _distance(self, vectora, vectorb):
        return abs(np.linalg.norm(vectora-vectorb))

    def _min_distance(self, trackleta, trackletb):
        a_features = trackleta.features
        b_features = trackletb.features

        # bruteforce solution, can be optimized
        min_distance = np.inf
        for i in range(len(a_features)):
            for j in range(len(b_features)):
                distance = self._distance(a_features[i], b_features[j])
                if distance < min_distance:
                    min_distance = distance

        return min_distance

    def draw_graph(self):
        nx.draw(self.graph, node_size=5, with_labels=False)
        plt.show()

    def build_links(self):
        self._build_lt_links()
        self._build_lc_links()
        tracks = []

        # extract subgraphs -> each subgraph is a track
        subgraphs = nx.connected_components(self.graph)
        for subgraph in subgraphs:
            tracklets = []
            for tracklet in subgraph:
                tracklets.append(tracklet)
            newtrack = track.Track(tracklets)
            tracks.append(newtrack)

        return tracks

    # lt links are built between tracklets in the large group
    # tracklet is built if min distance between any two frames of the tracklets is below a threshold
    def _build_lt_links(self):
        for trackleta in self.large_group:
            for trackletb in self.large_group:
                if (trackleta != trackletb):
                   if(self._min_distance(trackleta, trackletb)< self.params["lt_threshold"]):
                       print("Building Lt Edge", trackleta.color, trackletb.color)
                       self.graph.add_edge(trackleta, trackletb)

    def _build_lc_links(self):
        tracklets = self.small_group+self.large_group

        # First, generate sets of coexisting tracklets
        sets = self._get_coexisting_tracklets(tracklets)
        # Pairwise compare sets
        for seta in sets:
            for setb in sets:
                if seta!=setb:
                    self._compare_sets_and_build_links(seta, setb)

    def _compare_sets_and_build_links(self, seta, setb):
        # First, we need to make sure that each set is valid to build links to
        # This is an implementation of lambda^r, defined on the bottom left of
        # page 542
        if not self._set_can_be_compared(seta):
            return
        if not self._set_can_be_compared(setb):
            return

        # If each set is valid, we can follow the same process as lt link building
        for trackleta in seta:
            for trackletb in setb:
                if (trackleta != trackletb):
                    if (self._min_distance(trackleta, trackletb) < self.params["lt_threshold"]):
                        print("Building Lc Edge", trackleta.color, trackletb.color)
                        self.graph.add_edge(trackleta, trackletb)

    def _set_can_be_compared(self, set):
        for tracklet1 in set:
            for tracklet2 in set:
                if tracklet1 != tracklet2:
                    distance = self._min_distance(tracklet1, tracklet2)
                    if distance < self.params["lc_invalid_set_threshold"]:
                        return False
        return True

    def _get_coexisting_tracklets(self, tracklets):
        sets = []

        for tracklet in tracklets:
            # Run through all sets to see where this one belongs
            # A tracklet may be added to multiple coexisting sets
            addedToSet = False
            for set in sets:
                if self._coexisting_with_all_tracklets_in_set(tracklet, set):
                    set.append(tracklet)
                    addedToSet = True

            # If it doesn't belong in any coexisting set, create a new set
            if not addedToSet:
                sets.append([tracklet])

        return sets

    def _coexisting_with_all_tracklets_in_set(self, tracklet, set):
        for elem in set:
            if not tracklet.isCoexisting(elem):
                return False
        return True