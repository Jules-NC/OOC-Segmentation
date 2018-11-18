import collections

ImageSize = collections.namedtuple('ImageSize', ['len_x', 'len_y'])
Boundary = collections.namedtuple('Boundary', ['x1', 'y1', 'x2', 'y2'])


def boundary_to_image_size(boundary):
    """
    Convert a Boundary object to a ImageSize one

    :param boundary: A Boundary object
    :return: The size of the boundary
    """
    return ImageSize(boundary.x2 - boundary.x1 + 1, boundary.y2 - boundary.y1 + 1)
