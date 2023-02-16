import itertools
import math
import operator
import random
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation
from shapely import LineString, MultiLineString, Polygon, MultiPolygon

# Const values
PAUSE = 1.8


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


def get_status(current_node, nearest_node, distances):
    """
    Print all the data step-by-step

    :param current_node: (Node)
    :param nearest_node: (Node)
    :param distances: (dict of distances between current_node and all the nodes)

    """

    print("\nCurrent node: ", current_node.get_label())
    print("Distances: ", distances)
    print("Nearest node: ", nearest_node.get_label())
    print("Edge between: ", current_node.get_label(), "-", nearest_node.get_label())


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

        if len(_node_distance) != 0:  # if there are no edges left return None --> ends generate_edges recursion
            min_label = min(_node_distance, key=_node_distance.get)
        else:
            return None, None

        # TODO: tramite il dizionario _node_distance considerare prima il nodo più vicino, se c'è intersezione allora passa a quello dopo!
        # if len(_node_distance) != 0:    # if there are no edges left return None --> ends generate_edges recursion
        #     # min_label = min(_node_distance, key=_node_distance.get)
        #     min_labels = sorted(_node_distance.items(), key=itemgetter(1))[:2]
        # else:
        #     return None, None
        #
        # # TODO: tramite il dizionario _node_distance considerare prima il nodo più vicino, se c'è intersezione allora passa a quello dopo!
        # if self.check_edge_intersection(input_node, self._nodes[int(min_labels[0][0])]) is False:
        #     return self._nodes[int(min_labels[0][0])], _node_distance
        # else:
        #     return self._nodes[int(min_labels[1][0])], _node_distance

        return self._nodes[int(min_label)], _node_distance

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

    def check_edge_intersection(self, nodeA, nodeB):
        """
        Given two nodes it checks if the edge between the two nodes intersect other edges of the graph

        :param nodeA: (Node)
        :param nodeB: (Node)
        :return: bool

        """
        # Costruisco tutte le possibili combinazioni degli archi del grafo
        coords_combinations = {}
        for node1, node2 in itertools.combinations(self._nodes, 2):
            coords_combinations[(node1.get_label(), node2.get_label())] = ((node1.get_x(), node1.get_y()),
                                                                           (node2.get_x(), node2.get_y()))
        input_edge = ((nodeA.get_x(), nodeA.get_y()),
                      (nodeB.get_x(), nodeB.get_y()))

        for edge in self._graph.edges:
            if lines_intersect(input_edge[0], input_edge[1], coords_combinations[edge][0],
                               coords_combinations[edge][1]):
                print("{} e {} intersecano {} e {}".format(nodeA.get_label(), nodeB.get_label(),
                                                           coords_combinations[edge][0], coords_combinations[edge][1]))
                return True

        return False

    def generate_edges(self, central_node):
        """
        Generates the edges of the given graph starting from central_node and finding the nearest node to it. Then
        recursively applies the function to the new central_node until there are no more connections left in the graph

        """

        nearest_node, distances = self.find_nearest_node(central_node)

        if len(self.edges) < 2:
            self.build_edge(central_node, nearest_node)
            get_status(central_node, nearest_node, distances)
            self.visualize()

            return self.generate_edges(nearest_node)

        for u, v in self.edges:
            if nearest_node is not None:
                if not get_line_intersection(self._points[nearest_node.get_label()], self._points[central_node.get_label()],
                                       self._points[u], self._points[v]):   # FIXME: detecta intersezione tra le linee non tra i segmenti!

                    if not self.check_edge(central_node, nearest_node):
                        self.find_nearest_node(central_node)
                        self.build_edge(central_node, nearest_node)
                        get_status(central_node, nearest_node, distances)
                        self.visualize()

                        return self.generate_edges(nearest_node)

                    else:
                        continue

            else:
                return

        # nearest_node = self.new_edge_generation(central_node)
        #
        # return self.new_edge_generation(nearest_node)

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
        res = "--- Nodes ---"

        res += "\n"
        for node in self._nodes:
            res += str(node.get_label()) + ": "
            res += "x: " + str(node.get_x())
            res += " y: " + str(node.get_y()) + "\n"

        return res
