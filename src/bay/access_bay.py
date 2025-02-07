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

class AccessBay():
    def __init__(self, x: int, y: int, state: np.ndarray, access_points: list):
        # position of the north-west stack
        self.x = x
        self.y = y

        self.state = state
        self.width = state.shape[1]
        self.length = state.shape[0]
        if len(state.shape) == 2:
            self.height = 1
        else:
            self.height = state.shape[2]
        self.access_points = access_points
        self.virtual_lanes = None

    def __str__(self):
        return '{0}x{1} Bay at row {2}, column {3}, access_points {4}'.format(
            self.width, self.length, self.y, self.x, [point.ap_id for point in self.access_points]
        )

    def to_data_dict(self):
        data = dict()
        data['x'] = self.x
        data['y'] = self.y
        data['width'] = self.width
        data['length'] = self.length
        data['access_directions'] = list({point.direction for point in self.access_points})
        data['access_point_ids'] = [point.ap_id for point in self.access_points]
        return data

    def get_id(self):
        return str(self)