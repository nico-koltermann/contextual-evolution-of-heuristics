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


import time
import numpy as np
import sys
import types
import warnings

from .prompts import GetPrompts

import itertools

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DIMENSION_TO_SOLVE = 8

def cap_set_evaluate(priority, n: int) -> int:
  """Returns the size of an `n`-dimensional cap set."""
  capset = solve(priority, n)
  return len(capset)


def solve(priority, n: int) -> np.ndarray:
  """Returns a large cap set in `n` dimensions."""
  all_vectors = np.array(list(itertools.product((0, 1, 2), repeat=n)), dtype=np.int32)

  # Powers in decreasing order for compatibility with `itertools.product`, so
  # that the relationship `i = all_vectors[i] @ powers` holds for all `i`.
  powers = 3 ** np.arange(n - 1, -1, -1)

  # Precompute all priorities.
  priorities = np.array([priority.select_next_element(tuple(vector), n) for vector in all_vectors])

  # Build `capset` greedily, using priorities for prioritization.
  capset = np.empty(shape=(0, n), dtype=np.int32)
  while np.any(priorities != -np.inf):
    # Add a vector with maximum priority to `capset`, and set priorities of
    # invalidated vectors to `-inf`, so that they never get selected.
    max_index = np.argmax(priorities)
    vector = all_vectors[None, max_index]  # [1, n]
    blocking = np.einsum('cn,n->c', (- capset - vector) % 3, powers)  # [C]
    priorities[blocking] = -np.inf
    priorities[max_index] = -np.inf
    capset = np.concatenate([capset, vector], axis=0)

  return capset


class CAP_SET_CONST:
    def __init__(self, code_string = None):
        """
        Initializes the reshuffle evaluation with a heuristic code string and instance count.

        Parameters:
        - code_string (str): Heuristic function as a string.
        """
        self.prompts = GetPrompts()

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

                # Now you can use the module as you would any other
                fitness = cap_set_evaluate(heuristic_module, DIMENSION_TO_SOLVE)

                print(f"--- Fitness --- {fitness}")

                return fitness

        except Exception as e:
             #print("Error:", str(e))
             return None

if __name__ == "__main__":

    code_string = """ """

    start_time = time.time()
    reshuffle_const = CAP_SET_CONST(code_string)

    end_time = time.time()

    if reshuffle_const.fitness is not None:
        print("Fitness Score:", reshuffle_const.fitness)
    else:
        print("Evaluation failed due to an error in the provided heuristic code.")

    print("Total Execution Time:", end_time - start_time, "seconds")
