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


from src.bay.access_bay import AccessBay

def next_in_direction(bay : AccessBay, point : tuple, direction : str):
        """
        Gets next stack from access direction
        
        Parameters:
        bay (AccessBay): the bay to search in
        point (tuple): Y,X coordinates of the current stack
        direction (str): access direction

        Returns:
        tuple: the next point from this access direction 
            or None if reaches the end
        """
        length, width, height = bay.state.shape

        if point[0] < 0 or point[0] >= length:
            raise ValueError('Invalid Y coordinate: ' + str(point))

        if point[1] < 0 or point[1] >= width:
            raise ValueError('Invalid X coordinate: ' + str(point))

        if direction == 'north':
            if point[0] == length - 1:
                return None
            else:
                return (point[0] + 1, point[1])
        elif direction == 'south':
            if point[0] == 0:
                return None
            else:
                return (point[0] - 1, point[1])
        elif direction == 'west':
            if point[1] == width - 1:
                return None
            else:
                return (point[0], point[1] + 1)
        elif direction == 'east':
            if point[1] == 0:
                return None
            else:
                return (point[0], point[1] - 1)

        raise ValueError('Invalid direction')
