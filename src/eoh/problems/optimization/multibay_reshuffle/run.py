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
import sys
import time
import types
import datetime
import warnings
import numpy as np

from .prompts import GetPrompts

from src.util.eoh_util import (
    load_experiments,
    get_access_directions,
    create_virtual_lane)

from src.bay.warehouse import Warehouse

from src.util.eoh_util import (
    get_virtual_lane_score,
    convert_vl_to_list,
    create_lanes)

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


MAX_NUMBER_OF_MOVES = 100
TIMEOUT_SECONDS = 60
USE_REFERENCE_SOLUTION = True


def mutlibay_reshuffeling(priority, wh: Warehouse):

    start = datetime.datetime.now()
    current_move_number = 0

    while (get_virtual_lane_score(convert_vl_to_list(wh.virtual_lanes)) > 0
           and start.second + TIMEOUT_SECONDS > datetime.datetime.now().second
           and current_move_number < MAX_NUMBER_OF_MOVES):

        possible_lanes, _ = create_lanes(wh)

        virtual_lane_as_list = [convert_vl_to_list(inst) for inst in possible_lanes]

        fs_prio = priority.select_next_move(virtual_lane_as_list)

        selection_index = np.argmax(fs_prio)

        wh.virtual_lanes = possible_lanes[selection_index]

        current_move_number += 1

    return current_move_number

def eval_multibay_reshuffle(next_move, instance_configs, ref_scores):
    path = os.path.join(os.getenv('BASE_PATH'), 'warehouse_layouts')
    
    number_of_exp = len(instance_configs)

    detailed_fitness =  []
    h_initials =  []
    algo_moves =  []
    eval_times = []

    overall_score = 0

    for i, config in enumerate(instance_configs):

        access_directions = get_access_directions(config)
        wh = Warehouse(os.path.join(path, config['layout_file']), access_directions)
        wh.virtual_lanes = create_virtual_lane(config)

        eval_start_time = time.perf_counter()
        current_score = 0
        if USE_REFERENCE_SOLUTION:
            score = mutlibay_reshuffeling(next_move, wh)

            # Don't divide zero
            if score == 0:
                # if ref_score is also zero, then overall score is 0 and nothing added.
                # Otherwise, the solution is wrong and 1 is added.
                if ref_scores[i] != 0:
                    current_score = 1
            else:
                current_score = (score - ref_scores[i]) / ref_scores[i]

        else:
            current_score = mutlibay_reshuffeling(next_move, wh)

        algo_moves.append(score)
        h_initials.append(ref_scores[i])
        detailed_fitness.append(current_score)
        eval_times.append(time.perf_counter() - eval_start_time)
        overall_score += current_score

    details = {
        'detailed_fitness': detailed_fitness,
        'moves': algo_moves,
        'reference': h_initials,
        "eval_time": eval_times
    }

    return (overall_score / number_of_exp), details


class MULTIBAY_RESHUFFLECONST:
    def __init__(self, eoh_experiment_file, code_string = None):
        """
        Initializes the reshuffle evaluation with a heuristic code string and instance count.

        Parameters:
        - code_string (str): Heuristic function as a string.
        """
        self.prompts = GetPrompts()

        self.instance_configs, self.ref_scores = load_experiments(eoh_experiment_file)

        if len(self.instance_configs) == 0:
            print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            print("[INSTANCES ERROR]: No Instances available")
            print("[INSTANCES ERROR]: Make sure instances exists in correct folder and unpacked!")
            print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            exit(1)

        if code_string != None:
            self.fitness = self.evaluate(code_string)

    def evaluate(self, code_string):
        try:
            # Suppress warnings
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                # Create a new module object
                heuristic_module = types.ModuleType("heuristic_module")

                # Execute the code string in the new module's namespace
                exec(code_string, heuristic_module.__dict__)

                # Add the module to sys.modules so it can be imported
                sys.modules[heuristic_module.__name__] = heuristic_module

                try:
                    # Now you can use the module as you would any other
                    fitness, details = eval_multibay_reshuffle(heuristic_module, self.instance_configs, self.ref_scores)
                except Exception as e:
                    print(f"Error in Evaluation: {e}")

                print(f"--- Fitness --- {fitness}")

                return fitness, details

        except Exception as e:
             return None

if __name__ == "__main__":

    code_string = """
def select_next_move(warehouse_states):
    scores = []
    for state in warehouse_states:
        score = 0
        reshuffles = 0
        accessible_high_priority = 0
        for aisle_index, aisle in enumerate(state):
            for level_index, level in enumerate(aisle):
                if level != 0:
                    priority = level
                    blocking_factor = sum([
                        abs(level - upper_level) 
                        for upper_level in aisle 
                        if upper_level > priority
                    ])
                    score += priority - (blocking_factor * (level_index + 1)) 
                    if blocking_factor == 0:
                        accessible_high_priority += priority
                    if blocking_factor > 0:
                        reshuffles += (level_index + 1) * (aisle_index + 1)
        scores.append(score + accessible_high_priority - reshuffles)
    return scores
"""

    start_time = time.time()
    eoh_experiment_file = "exp_1.json"
    reshuffle_const = MULTIBAY_RESHUFFLECONST(eoh_experiment_file, code_string)

    end_time = time.time()

    if reshuffle_const.fitness is not None:
        print("Fitness Score:", reshuffle_const.fitness)
    else:
        print("Evaluation failed due to an error in the provided heuristic code.")

    print("Total Execution Time:", end_time - start_time, "seconds")
