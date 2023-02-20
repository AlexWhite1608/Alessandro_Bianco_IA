# ---------- Taken from https://martin-thoma.com/how-to-check-if-two-line-segments-intersect/#Where_do_two_line_segments_intersect ---------#


# A small value used to handle floating-point arithmetic errors
EPSILON = 1e-9


def get_bounding_box(segment):
    x1, y1 = segment[0]
    x2, y2 = segment[1]
    return [
        (min(x1, x2), min(y1, y2)),
        (max(x1, x2), max(y1, y2))
    ]


def do_bounding_boxes_intersect(a1, a2, b1, b2):
    box1 = get_bounding_box((a1, a2))
    box2 = get_bounding_box((b1, b2))

    return box1[0][0] <= box2[1][0] and \
           box1[1][0] >= box2[0][0] and \
           box1[0][1] <= box2[1][1] and \
           box1[1][1] >= box2[0][1]


def is_point_on_line(p1, p2, p=None):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    p1_tmp = (0, 0)
    p2_tmp = (dx, dy)
    p_tmp = (p[0] - p1[0], p[1] - p1[1])
    r = cross_product(p2_tmp, p_tmp)
    return abs(r) < EPSILON


def is_point_right_of_line(p1, p2, p=None):
    a_tmp = (0, 0)
    b_tmp = (p2[0] - p1[0], p2[1] - p1[1])
    c_tmp = (p[0] - p1[0], p[1] - p1[1])
    return cross_product(b_tmp, c_tmp) < 0


def line_segment_crosses_line(a, b):
    return is_point_right_of_line(a[0], a[1], b[0]) != is_point_right_of_line(a[0], a[1], b[1])


def cross_product(u, v):
    return u[0] * v[1] - u[1] * v[0]

# -------------------#
