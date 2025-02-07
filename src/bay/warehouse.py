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
from typing import List

from src.bay.access_bay import AccessBay
from src.bay.access_point import AccessPoint
from src.preprocessing.layout_to_bays import layout_to_bays
from src.util.access_util import next_in_direction
from src.util.graph_distance_estimator import edges_to_neighbors
from src.util.graph_distance_estimator import estimate_distances_bfs

class Warehouse:
    def __init__(self, filename: str, access_directions : dict):
        """
        Generates a Warehouse object based on a given layout. 
        Doesn't generate the stacks, leaves the bays empty.
        """
        dictionary = layout_to_bays(filename, access_directions)
        self.bays = dictionary["bays"]
        self.path_nodes = dictionary["path_nodes"]
        self.edges = dictionary["edges"]
        self.length = dictionary["length"]
        self.width = dictionary["width"]
        self.sinks = dictionary["sinks"]
        self.sources = dictionary["sources"]
        self.neighbors = edges_to_neighbors(self.edges)

        # Only used in viz
        self.ap_distance = estimate_distances_bfs(self.unpack_access_points(), self.neighbors)

        self.virtual_lanes = None

        self.all_access_points = []
        ap_id_offset = 0

        if self.has_sources():
            for source in self.sources: 
                self.all_access_points.extend(source.access_points)
                for i in range(len(source.access_points)):
                    source.access_points[i].ap_id = i + ap_id_offset
                ap_id_offset += len(source.access_points)

        for bay in self.bays:
            self.all_access_points.extend(bay.access_points)
            for i in range(len(bay.access_points)):
                bay.access_points[i].ap_id = i + ap_id_offset
            ap_id_offset += len(bay.access_points)

        if self.has_sinks():
            for sink in self.sinks: 
                self.all_access_points.extend(sink.access_points)
                for i in range(len(sink.access_points)):
                    sink.access_points[i].ap_id = i + ap_id_offset
                ap_id_offset += len(sink.access_points)
        
    def __apply_move(self, move: tuple):
        remove_i, _ = self.get_vl_index_for_ap(move[0])
        add_i, _ = self.get_vl_index_for_ap(move[1])
        try:
            self.virtual_lanes[remove_i], stacks = self.virtual_lanes[remove_i].remove_load()
            self.virtual_lanes[add_i] = self.virtual_lanes[add_i].add_load(stacks)
        except Exception as e:
            print(e)
            print("CANNOT MOVE IN WH")

    def get_vl_index_for_ap(self, ap: int):
        for index, vl in (enumerate(self.virtual_lanes)):
            if vl.ap_id == ap:
                return index, vl
        return None


    def get_valid_moves(self):
        from_lanes = self.get_moveable_unit_loads()
        to_lanes = self.lanes_with_free_loads()

        moves = []

        for from_lane in from_lanes:
            for to_lane in to_lanes:
                # prevent moves that do nothing (use the same lane)
                if from_lane == to_lane:
                    continue

                moves.append((from_lane, to_lane))

        return moves

    def lanes_with_free_loads(self) -> List[int]:
        """
        Returns:
        (list): list of indices of lanes that contain some loads.
        """

        if self.virtual_lanes is None:
            raise 'No virtual lanes in warehouse! Object is None'

        return [vl.ap_id for vl in self.virtual_lanes if vl.has_free_loads()]

    def get_moveable_unit_loads(self) -> List[int]:
        """
        Returns:
        (list): list of indices of lanes that contain some loads.
        """

        if self.virtual_lanes is None:
            raise 'No virtual lanes in warehouse! Object is None'

        return [vl.ap_id for vl in self.virtual_lanes if vl.has_loads()]

    def lanes_with_slots(self) -> List[int]:
        """
        Returns:
        (list): list of indices of lanes that contain some free slots.
        """
        if self.virtual_lanes is None:
            raise 'No virtual lanes in warehouse! Object is None'

        return [vl.ap_id for vl in self.virtual_lanes if vl.has_slots()]


    def update_warehouse(self, move):
        self.__apply_move(move)
        self.read_lanes(self.virtual_lanes)

    def read_lanes(self, lanes):
        for lane in lanes:
            ap: AccessPoint = self.all_access_points[lane.ap_id]
            bay: AccessBay = ap.bay
            stack = ap.get_stack_yx()
            for i in range(len(lane.stacks) // bay.height):
                start = bay.height * i
                end = start + bay.height
                bay.state[stack] = lane.stacks[start:end]
                stack = next_in_direction(bay, stack, ap.direction)

    def get_ap_from_vl(self, point: int):
        return self.virtual_lanes[point].ap_id

    def estimate_fill_level(self):
        n_loads = 0
        total = 0

        for bay in self.bays:
            n_loads += np.count_nonzero(bay.state)
            total += np.prod(bay.state.shape)

        return n_loads / total

    def unpack_access_points(self):
        """
        Unpacks all access points into a single list of (y,x) tuples preserving the order. 
        If adding things like sinks and sources to the warehouse, put them into a list like below
        """
        baysAndSinksAndSources = self.sources+ self.bays + self.sinks
        access_points_by_bay = [[ap.get_global_yx() for ap in bay.access_points] for bay in baysAndSinksAndSources]
        all_access_points = []
        for ap_list in access_points_by_bay:
            # Todo: Object needs to be added?
            # ap = AccessPoint() # global_x, global_y, stack_x: int, stack_y: int, direction: str
            all_access_points.extend(ap_list)

        return all_access_points

    def has_sinks(self):
        if len(self.sinks) > 0: 
            return True
        return False
    
    def has_sources(self):
        if len(self.sources) > 0: 
            return True
        return False

    def get_state_as_arry(self):
        return [x for bay in self.bays for state in bay.state for s in state for x in s]