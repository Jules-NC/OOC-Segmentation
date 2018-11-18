import collections

ImageLen = collections.namedtuple('ImageLen', ['len_x', 'len_y'])
Boundary = collections.namedtuple('Boundary', ['x1', 'y1', 'x2', 'y2'])


def bound_to_imglen(boundary):
    """
    Convert a Boundary object to a ImageSize one

    :param boundary: A Boundary object
    :return: The size of the boundary
    """
    return ImageLen(boundary.x2 - boundary.x1 + 1, boundary.y2 - boundary.y1 + 1)
