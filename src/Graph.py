import itertools
import math
import operator
import random
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation
from shapely import LineString, MultiLineString, Polygon, MultiPolygon

# Const values
PAUSE = 1.5

# A small value used to handle floating-point arithmetic errors
EPSILON = 1e-9


def create_random_nodes(n_nodes):
    """
    Creates n_nodes Node class instances with random x,y coordinates.

    :param: n_nodes (int)
    :return: list of Node

    """

    nodes = []
    for i in range(n_nodes):
        x = random.randint(1, 100)
        y = random.randint(1, 100)
        label = str(i)
        nodes.append(Node(label, x, y))

    return nodes


def lines_intersect(p, q, r, s):
    return (ccw(p, r, s) != ccw(q, r, s)) and (ccw(p, q, r) != ccw(p, q, s))


def ccw(p, q, r):
    return (r[1] - p[1]) * (q[0] - p[0]) > (q[1] - p[1]) * (r[0] - p[0])


def get_line_intersection(p0, p1, p2, p3):
    s1_x = p1[0] - p0[0]
    s2_x = p3[0] - p2[0]

    s1_y = p1[1] - p0[1]
    s2_y = p3[1] - p2[1]

    s = (-s1_y * (p0[0] - p2[0]) + s1_x * (p0[1] - p2[1])) / (-s2_x * s1_y + s1_x * s2_y)
    t = (s2_x * (p0[1] - p2[1]) - s2_y * (p0[0] - p2[0])) / (-s2_x * s1_y + s1_x * s2_y)

    if 0 <= s <= 1 and 0 <= t <= 1:
        print(f"Collisione tra {p0} - {p1} e {p2} - {p3}")
        return True
    else:
        return False


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

    return box1[0][0] <= box2[1][0] and box1[1][0] >= box2[0][0] and box1[0][1] <= box2[1][1] and box1[1][1] >= box2[0][
        1]


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


def do_lines_intersect(a1, a2, b1, b2):
    line_segment_a = (a1, a2)
    line_segment_b = (b1, b2)

    # Nel caso in cui un estremo sia uguale per due segmenti allora ci va bene!
    if (a2 == b1) or (a1 == b2):
        return False

    if do_bounding_boxes_intersect(a1, a2, b1, b2) \
            and line_segment_crosses_line(line_segment_a, line_segment_b) \
            and line_segment_crosses_line(line_segment_b, line_segment_a):
        print(f"Intersezione tra {a1} - {a2} e {b1} - {b2}")
        return True

    return False


def cross_product(u, v):
    return u[0] * v[1] - u[1] * v[0]


class Node:
    def __init__(self, label, x, y):
        self._x = x
        self._y = y
        self._label = label

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_label(self):
        return self._label


class Graph:

    def __init__(self, n_nodes, save=False):
        """
        Builds the graph given n_nodes Nodes. It also sets the coordinates from each node to be used for the
        graph generation

        :param n_nodes (int)

        """
        self.n_nodes = n_nodes
        self._nodes = create_random_nodes(self.n_nodes)
        self.edges = []
        self.save = save
        self._points = self.get_dict_coords()

        self._graph = nx.Graph()

        for node in self._nodes:
            pos_x = node.get_x()
            pos_y = node.get_y()
            self._graph.add_node(node.get_label(), pos=(pos_x, pos_y))

        pos = self.get_dict_coords()
        nx.set_node_attributes(self._graph, pos, 'coord')

    def get_status(self, current_node, nearest_node):
        """
        Print all the data step-by-step

        :param current_node: (Node)
        :param nearest_node: (Node)

        """

        print("\nCurrent node: ", current_node.get_label(), ": ", f"{self._points[current_node.get_label()]}")
        print("Nearest node: ", nearest_node.get_label(), ": ", f"{self._points[nearest_node.get_label()]}")
        print("Edge between: ", current_node.get_label(), "-", nearest_node.get_label())

    def add_node(self, node):  # TODO: VANNO AGGIUNTI AL GRAFO!
        if node not in self._nodes:
            self._nodes.append(node)

    def remove_node(self, node):  # TODO: VANNO RIMOSSI DAL GRAFO!
        if node in self._nodes:
            self._nodes.remove(node)

    def get_random_node(self):
        node = random.choice(self._nodes)

        return node

    def check_edge(self, node1, node2):
        """
        Returns True if there is an edge between the two nodes, return False if there is not

        :param node1: (Node)
        :param node2: (Node)

        """
        edge1 = tuple((node1.get_label(), node2.get_label()))
        edge2 = tuple((node2.get_label(), node1.get_label()))

        if edge1 in self.edges or edge2 in self.edges:
            return True
        else:
            return False

    def find_nearest_node(self, input_node):
        """
        Returns the nearest node from the input_node using Euclidean distance. It must satisfy all the conditions!

        :param input_node (Node)
        :return: nearest node to input_node

        """
        _node_distance = {}
        for _node in self._nodes:
            if input_node != _node:
                if not self.check_edge(input_node, _node):  # if there is already an edge skip
                    _node_distance[_node.get_label()] = math.dist((input_node.get_x(), input_node.get_y()),
                                                                  (_node.get_x(), _node.get_y()))

        if len(_node_distance) == 0:  # if there are no edges left return None --> ends generate_edges recursion
            return None

        sorted_node_distances = sorted(_node_distance, key=_node_distance.get)

        # a list containing the nearest nodes to input_node sorted by distance
        distance_ordered_nodes = []
        for x in sorted_node_distances:
            for node in self._nodes:
                if x == node.get_label():
                    distance_ordered_nodes.append(node)

        return distance_ordered_nodes

    def get_dict_coords(self):
        """
        :return: a dict containing key: node, value: tuple of x,y coords

        """
        dict_coords = {}
        for node in self._nodes:
            dict_coords[node.get_label()] = tuple((node.get_x(), node.get_y()))

        return dict_coords

    def build_edge(self, node1, node2):
        """
        Builds an edge between node1 and node2 if they are not the same node

        :param node1: (Node)
        :param node2: (Node)
        """

        if node1 is not node2:
            self._graph.add_edge(node1.get_label(), node2.get_label())
            edge = tuple((node1.get_label(), node2.get_label()))

            if edge not in self.edges:
                self.edges.append((node1.get_label(), node2.get_label()))

    def generate_edges(self, central_node):
        """
        Generates the edges of the given graph starting from central_node and finding the nearest node to it. Then
        recursively applies the function to the new central_node until there are no more connections left in the graph

        """

        distance_ordered_nodes = self.find_nearest_node(central_node)

        if distance_ordered_nodes is None:    # No other nodes available
            return

        if len(self.edges) < 2:     # No need to check for intersections
            self.build_edge(central_node, distance_ordered_nodes[0])
            self.get_status(central_node, distance_ordered_nodes[0])
            self.visualize()

            return self.generate_edges(distance_ordered_nodes[0])

        for node, _ in enumerate(distance_ordered_nodes):
            if distance_ordered_nodes[node] is not None:

                if not self.check_edge(central_node, distance_ordered_nodes[node]):
                    if not any(do_lines_intersect(self._points[distance_ordered_nodes[node].get_label()],
                                                  self._points[central_node.get_label()], self._points[u],
                                                  self._points[v])
                               for u, v in self.edges):

                        # self.find_nearest_node(central_node)    #FIXME: serve??
                        self.build_edge(central_node, distance_ordered_nodes[node])
                        self.get_status(central_node, distance_ordered_nodes[node])

                        self.visualize()    #TODO: sarebbe figo se si potesse vedere che disegna comunque l'edge anche se c'è intersezione (in rosso) e poi lo cancella

                        return self.generate_edges(distance_ordered_nodes[node])

                    else:
                        continue

                else:
                    continue

            else:
                return

    def visualize(self):
        """
        Visualization of the given graph

        """
        if self.save:
            plt.savefig("graph.png")

        fig = plt.figure()
        plt.figure().clear()
        plt.close()
        plt.clf()

        nx.draw_networkx_edges(self._graph, nx.get_node_attributes(self._graph, 'pos'))
        nx.draw_networkx_nodes(self._graph, nx.get_node_attributes(self._graph, 'pos'), node_color='green')
        nx.draw_networkx_labels(self._graph, nx.get_node_attributes(self._graph, 'pos'), font_size=13)
        plt.show()
        plt.pause(PAUSE)

    def __str__(self):
        res = "\n--- Nodes ---"

        res += "\n"
        for node in self._nodes:
            res += str(node.get_label()) + ": "
            res += "x: " + str(node.get_x())
            res += " y: " + str(node.get_y()) + "\n"

        return res
