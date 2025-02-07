# Copyright (c) 2025
#           Thomas Bömer (thomas.bömer@tu-dortmund.de)
#           Nico Koltermann (nico.koltermann@tu-dortmund.de) 
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import numpy as np

from collections import defaultdict

def __dfs(start_node, neighbors, distance = None, parent = None):
    """dfs, probably unnecessary for this application"""
    if not distance:
        distance = {start_node : 0}
        parent = {start_node : None}
        child_distance = 0
    else:
        child_distance = distance[start_node] + 1
    for nbr in neighbors[start_node]:
        if not nbr in parent or distance[nbr] > child_distance:
            parent[nbr] = start_node
            distance[nbr] = child_distance
            __dfs(nbr, neighbors, distance, parent)
    return distance, parent

def __bfs(start_node, neighbors):
    """bfs, used to estimate all distances"""
    to_visit = [start_node]
    parent = {start_node : None}
    distance = {start_node : 0}
    
    while len(to_visit) > 0:
        node = to_visit.pop(0)
        for nbr in neighbors[node]:
            if not nbr in parent:
                to_visit.append(nbr)
                parent[nbr] = node
                distance[nbr] = distance[node] + 1
    
    return distance, parent

def estimate_distances_bfs(nodes, neighbors):
    """
    estimates distances between bays' access points

    nodes: list(tuple)
    neigbors: dict, with all nodes: [neighbor nodes]
    """
    
    graph_distance = np.zeros((len(nodes), len(nodes)))

    for i in range(len(nodes)):
        distance, _ = __bfs(nodes[i], neighbors)
        # assuming undirected graph
        for j in range(i+1, len(nodes)):
            graph_distance[i][j] = distance[nodes[j]]
            graph_distance[j][i] = distance[nodes[j]]
    
    return graph_distance

def edges_to_neighbors(edges):
    """
    turns edges of an undirected graph into a "neighbors" dictionary
    """
    neighbors = defaultdict(list)
    for edge in edges:
        neighbors[edge[0]].append(edge[1])
        neighbors[edge[1]].append(edge[0])
    return dict(neighbors)