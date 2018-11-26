import collections

ImageSize = collections.namedtuple('ImageSize', ['len_x', 'len_y'])


def boundary_to_image_size(boundary):
    """
    Convert a Boundary object to a ImageSize one

    :param boundary: A Boundary object
    :return: The size of the boundary
    """
    return ImageSize(boundary.x2 - boundary.x1 + 1, boundary.y2 - boundary.y1 + 1)


class Image:
    def __init__(self, x, y):
        self.len_x = x
        self.len_y = y


Image = Image(4, 2)
