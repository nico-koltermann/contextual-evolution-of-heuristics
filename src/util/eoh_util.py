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


import os
import json

import numpy as np
from src.util.paths_util import get_working_dir, read_all_json_files

from src.bay.virtual_lane import VirtualLane


def convert_list_to_vl(vl_list: list, ap_ids: list):
    virtual_lanes = []
    for i in range(len(vl_list)):
        new_lane = VirtualLane()
        new_lane.ap_id = ap_ids[i]
        new_lane.stacks = np.array(vl_list[i])
        virtual_lanes.append(new_lane)
    return virtual_lanes


def convert_vl_to_list(virtual_lanes):
    return [list(v.stacks) for v in virtual_lanes]


def get_ap_ids_from_vl(virtual_lanes: list):
    return [vl.ap_id for vl in virtual_lanes]


def get_virtual_lane_score(virtual_lanes: list, reversed=False):
    return sum([1 for lane in virtual_lanes if sorted(lane, reverse=reversed) != lane])


def get_access_directions(config):
    access_directions = config['bay_info']['0']['access_directions']
    return {
        "north": 'north' in access_directions,
        "east": 'east' in access_directions,
        "south": 'south' in access_directions,
        "west": 'west' in access_directions
    }


def load_experiments(file):
    instance_path = os.getenv('INSTANCES_PATH')
    experiment_path = os.path.join(os.getenv('BASE_PATH'), "eoh_experiment")

    experiment_instances = []
    experiment_solution = []

    try:
        f_exp = open(os.path.join(experiment_path, file))
        data = json.load(f_exp)
    except:
        print("[ERROR]: load_experiments failed - experiment file does not exists!")
        exit(1)

    for s in data["seed"]:
        for bay in data["bay"]:
            for warehouse in data["warehouse"]:
                for fill in data["fill"]:
                    for priority in data["priority"]:

                        try:
                            f_inst = open(os.path.join(instance_path,
                                                       f'test_file_Size_{bay}x{bay}_'
                                                       f'Layout_{warehouse}x{warehouse}_'
                                                       f'fill_lvl_{fill}_'
                                                       f'seed_{s}_'
                                                       f'max_p_{priority}_'
                                                       f'ad_access_directions_'
                                                       f'{data["access_directions"]}.json'))

                            instance = json.load(f_inst)
                            experiment_instances.append(instance)
                            experiment_solution.append(instance['h_initial'])

                        except:
                            print("[ERROR]: load_experiments failed - file does not exists!")
                            print(f"[ERROR]: seed: {s}, bay: {bay}, warehouse: {warehouse}, "
                                  f"fill: {fill}, priority: {priority}")
                            print("---> continue with other files...")

    return experiment_instances, experiment_solution


def generate_instances(number_of_instances: int, path=get_working_dir()) -> list:
    path = os.getenv('INSTANCES_PATH')
    all_files = read_all_json_files(path)

    if number_of_instances > len(all_files):
        raise Exception('Not enough experiment instances')

    instance_configs = []

    for i in range(number_of_instances):
        f = open(os.path.join(path, all_files[i]))
        data = json.load(f)
        instance_configs.append(data)

    return instance_configs


def create_virtual_lane(data):
    lanes = []
    for virtual_lane in data["virtual_lanes"]:
        new_lane = VirtualLane()
        new_lane.ap_id = virtual_lane["ap_id"]
        new_lane.stacks = np.array(virtual_lane["stacks"])
        lanes.append(new_lane)

    return lanes


def create_virtual_lane_reversed(data, max_value):
    lanes = []
    for virtual_lane in data["virtual_lanes"]:
        new_lane = VirtualLane()
        new_lane.ap_id = virtual_lane["ap_id"]

        # Reverse for LMM understanding
        new_lane.stacks = np.array(virtual_lane["stacks"])

        print(new_lane.stacks)

        new_lane.stacks = new_lane.stacks[::-1]

        # Flip the priorities
        new_lane.stacks = np.array([min(1, x) * abs(x - (max_value + 1)) for x in new_lane.stacks])

        print(new_lane.stacks)
        print()

        lanes.append(new_lane)

    return lanes


def create_lanes(wh, reversed=False):
    lanes = wh.virtual_lanes

    loads = []
    slots = []
    for i in range(len(lanes)):
        if np.any(lanes[i].stacks != 0):
            loads.append(i)
        if 0 in lanes[i].stacks:
            slots.append(i)

    successors = []
    moves = []
    from_lanes = loads
    to_lanes = slots
    for from_lane in from_lanes:
        for to_lane in to_lanes:

            if from_lane == to_lane:
                continue

            new_lane = lanes[:]
            if reversed:
                new_lane[from_lane], stacks = lanes[from_lane].remove_load_reversed()
                new_lane[to_lane] = lanes[to_lane].add_load_reversed(stacks)
            else:
                new_lane[from_lane], stacks = lanes[from_lane].remove_load()
                new_lane[to_lane] = lanes[to_lane].add_load(stacks)

            successors.append(new_lane)
            moves.append([lanes[from_lane].ap_id, lanes[to_lane].ap_id])

    return successors, moves
