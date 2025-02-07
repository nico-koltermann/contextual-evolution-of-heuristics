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


# ASSUMPTION: RECTANGULAR BAYS!!!
import sys
import os

wd = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(wd, '../..'))
from typing import List
import numpy as np

import csv

from src.bay.access_bay import AccessBay
from src.bay.access_point import AccessPoint
from src.bay.sink import Sink
from src.bay.source import Source

from src.util.paths_util import get_working_dir


def __read_layout(filename: str) -> np.ndarray:
    """parses the csv file into a numpy array"""
    base_path = os.path.join(os.getenv("BASE_PATH"), "warehouse_layouts")
    layout_file = "Size" + filename.split(r"Size")[-1]
    filename =  os.path.join(base_path, layout_file)

    with open(filename) as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.readline())
    strings = np.loadtxt(filename, delimiter=dialect.delimiter, dtype=str)
    if strings[0, -1] == '':
        strings = strings[:, :-1]
    layout = strings.astype(int)
    return layout


def __find_bays(layout: np.ndarray):
    """
    returns bays as a list
    """
    layout_length, layout_width = layout.shape
    is_stack = layout == 1
    bays = []
    for y in range(layout_length):
        for x in range(layout_width):
            if is_stack[y, x]:
                bay_length = 1
                while y + bay_length < layout_length and is_stack[y + bay_length, x]:
                    bay_length += 1

                bay_width = 1
                while x + bay_width < layout_width and is_stack[y, x + bay_width]:
                    bay_width += 1

                is_stack[y:y + bay_length, x:x + bay_width] = False
                bay = AccessBay(x, y, layout[y:y + bay_length, x:x + bay_width], None)
                bays.append(bay)
    return bays


def __find_sinks(layout: np.ndarray):
    """
    returns sinks as a list
    """
    layout_length, layout_width = layout.shape
    is_stack = layout == 2
    sinks = []
    for y in range(layout_length):
        for x in range(layout_width):
            if is_stack[y, x]:
                sink_length = 1
                while y + sink_length < layout_length and is_stack[y + sink_length, x]:
                    sink_length += 1

                sink_width = 1
                while x + sink_width < layout_width and is_stack[y, x + sink_width]:
                    sink_width += 1

                is_stack[y:y + sink_length, x:x + sink_width] = False
                sink = Sink(x, y, layout[y:y + sink_length, x:x + sink_width], None)
                sinks.append(sink)
    return sinks


def __find_sources(layout: np.ndarray):
    """
    returns sources as a list
    """
    layout_length, layout_width = layout.shape
    is_stack = layout == 3
    sources = []
    for y in range(layout_length):
        for x in range(layout_width):
            if is_stack[y, x]:
                source_length = 1
                while y + source_length < layout_length and is_stack[y + source_length, x]:
                    source_length += 1

                source_width = 1
                while x + source_width < layout_width and is_stack[y, x + source_width]:
                    source_width += 1

                is_stack[y:y + source_length, x:x + source_width] = False
                source = Source(x, y, layout[y:y + source_length, x:x + source_width], None)
                sources.append(source)
    return sources


def __find_paths(layout: np.ndarray):
    """
    returns path as a graph (path nodes and edges)
    """
    is_path = np.logical_or(layout == -5, layout == -6)
    Y_p, X_p = np.where(is_path)
    path_nodes = np.hstack((np.reshape(Y_p, (-1, 1)), np.reshape(X_p, (-1, 1))))
    path_edges = []
    for i in range(len(path_nodes)):
        for j in range(i + 1, len(path_nodes)):
            if abs(path_nodes[i][0] - path_nodes[j][0]) + abs(path_nodes[i][1] - path_nodes[j][1]) == 1:
                edge = tuple(path_nodes[i]), tuple(path_nodes[j])
                path_edges.append(edge)
    return path_nodes, path_edges


def __find_access_points(layout: np.ndarray, bays: List, access_directions: dict):
    layout_length, layout_width = layout.shape
    is_path = (layout == -5)
    for bay in bays:
        bay_aps = []

        # north
        if access_directions["north"]:
            for i in range(bay.width):
                if bay.y - 1 < 0:
                    break
                if is_path[bay.y - 1, bay.x + i]:
                    ap = AccessPoint(bay, bay.x + i, bay.y - 1, i, 0, 'north')
                    bay_aps.append(ap)

        # south
        if access_directions["south"]:
            for i in range(bay.width):
                if bay.y + bay.length >= layout_length:
                    break
                if is_path[bay.y + bay.length, bay.x + i]:
                    ap = AccessPoint(bay, bay.x + i, bay.y + bay.length, i, bay.length - 1, 'south')
                    bay_aps.append(ap)

        # west
        if access_directions["west"]:
            for j in range(bay.length):
                if bay.x - 1 < 0:
                    break
                if is_path[bay.y + j, bay.x - 1]:
                    ap = AccessPoint(bay, bay.x - 1, bay.y + j, 0, j, 'west')
                    bay_aps.append(ap)

        # east
        if access_directions["east"]:
            for j in range(bay.length):
                if bay.x + bay.width >= layout_width:
                    break
                if is_path[bay.y + j, bay.x + bay.width]:
                    ap = AccessPoint(bay, bay.x + bay.width, bay.y + j, bay.width - 1, j, 'east')
                    bay_aps.append(ap)

        bay.access_points = bay_aps


def layout_to_bays(filename: str, access_directions: dict):
    """
    Parses a layout into bays and path graph

    Returns a dictionary containing lists of bays, sinks, path nodes and edges and the dimensions of the layout
    """
    layout = __read_layout(filename)
    sources = __find_sources(layout)
    bays = __find_bays(layout)
    sinks = __find_sinks(layout)
    # We hardcode the access directions for the sink and source here to be true just for the north direction
    # If you want to use the access directions from the layout file, you have to change this here:
    sinkAndSourceAccessDirections = {"north": True, "east": False, "south": False, "west": False}
    __find_access_points(layout, sources, sinkAndSourceAccessDirections)
    __find_access_points(layout, bays, access_directions)
    __find_access_points(layout, sinks, sinkAndSourceAccessDirections)
    path_nodes, path_edges = __find_paths(layout)
    return {
        "bays": bays,
        "path_nodes": path_nodes,
        "edges": path_edges,
        "length": len(layout),
        "width": len(layout[0]),
        "sinks": sinks,
        "sources": sources
    }


if __name__ == '__main__':
    filename = "../../examples/Size_3x3_Layout_2x2_sink_source.csv"
    access_directions = {"north": True, "east": True, "south": True, "west": True}
    dictionary = layout_to_bays(filename, access_directions)
    print(dictionary)
    print(dictionary["sources"][0])
    print(dictionary["sinks"][0])
    print(dictionary["bays"][0])
