# ---------- Taken from https://martin-thoma.com/how-to-check-if-two-line-segments-intersect/#Where_do_two_line_segments_intersect ---------#


# A small value used to handle floating-point arithmetic errors
EPSILON = 1e-9


def get_bounding_box(segment):

    """
    Return the bounding box that surrounds the given segment

    :param segment: A tuple containing the start/end point coordinates of the segment
    :return: A tuple containing the bounding box

    """

    x1, y1 = segment[0]
    x2, y2 = segment[1]
    return [
        (min(x1, x2), min(y1, y2)),
        (max(x1, x2), max(y1, y2))
    ]


def do_bounding_boxes_intersect(a1, a2, b1, b2):

    """
    Check if bounding boxes do intersect. If one bounding box touches the other, they do intersect.

    :param a1: (tuple of x/y coordinates) First point of the first bounding box
    :param a2: (tuple of x/y coordinates) Second point of the first bounding box
    :param b1: (tuple of x/y coordinates) First point of the second bounding box
    :param b2: (tuple of x/y coordinates) Second point of the second bounding box
    :return: True if they intersect, False otherwise

    """

    box1 = get_bounding_box((a1, a2))
    box2 = get_bounding_box((b1, b2))

    return box1[0][0] <= box2[1][0] and \
           box1[1][0] >= box2[0][0] and \
           box1[0][1] <= box2[1][1] and \
           box1[1][1] >= box2[0][1]


def is_point_on_line(p1, p2, p=None):

    """

    Check if the point p is on the line described by the two points p1 and p2

    :param p1: (tuple) Coordinates of the first point that generates the line
    :param p2: (tuple) Coordinates of the second point that generates the line
    :param p:  (tuple) Coordinates of the point that we want to check
    :return: True if point is on the line, False otherwise

    """

    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    p2_tmp = (dx, dy)
    p_tmp = (p[0] - p1[0], p[1] - p1[1])
    r = cross_product(p2_tmp, p_tmp)
    return abs(r) < EPSILON


def is_point_right_of_line(p1, p2, p=None):

    """

    Check if a point is right of a line. If the point is on the line, it is not right of the line.

    :param p1: (tuple) Coordinates of the first point that generates the line
    :param p2: (tuple) Coordinates of the second point that generates the line
    :param p:  (tuple) Coordinates of the point that we want to check
    :return: True if point is right of the line, False otherwise

    """

    b_tmp = (p2[0] - p1[0], p2[1] - p1[1])
    c_tmp = (p[0] - p1[0], p[1] - p1[1])
    return cross_product(b_tmp, c_tmp) < 0


def line_segment_crosses_line(a, b):

    """

    Check if the first line a crosses the second line b

    :param a: (tuple) Coordinates of the two points that generates the first line
    :param b: (tuple) Coordinates of the two points that generates the second line
    :return: True if the first line crosses the second one, False otherwise

    """

    return is_point_right_of_line(a[0], a[1], b[0]) != is_point_right_of_line(a[0], a[1], b[1])


def cross_product(u, v):

    """

    Return the cross product between the two points u and v

    :param u: (tuple) coordinates of the first point
    :param v: (tuple) coordinates of the second point
    :return: The cross product
    """

    return u[0] * v[1] - u[1] * v[0]

# -------------------#
