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


class InstanceLoader(): 
    def __init__(self, instance): 
        self.n = 1
        self.file = instance["layout_file"].split("/")[-1].split(".")[0]
        self.fill_level = instance["fill_level"]
        self.max_priority = instance["max_priority"]
        self.height = instance["height"]
        self.seed = instance["seed"]
        self.access_directions = self._create_access_directions_dict(instance["bay_info"]["0"]["access_directions"])

    def _create_access_directions_dict(self, access_directions): 
        north, east, south, west = False, False, False, False
        if "north" in access_directions: 
            north = True
        if "east" in access_directions: 
            east = True
        if "south" in access_directions: 
            south = True
        if "west" in access_directions: 
            west = True
        return {
            "north": north, 
            "east" : east,
            "south": south,
            "west" : west
        }