import math
import random
import networkx as nx
import matplotlib.pyplot as plt
import Intersections as intx

# Const values
PAUSE = 1.0


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

        print("\nCurrent node:", current_node.get_label(), f"{self._points[current_node.get_label()]}")
        print("Nearest node:", nearest_node.get_label(), f"{self._points[nearest_node.get_label()]}")
        print("Edge between:", current_node.get_label(), "-", nearest_node.get_label())

    def get_random_node(self):
        return random.choice(self._nodes)

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

    def get_node_from_coords(self, coords):

        for node, coordinates in self._points.items():
            if coords == coordinates:
                return node

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

    def do_lines_intersect(self, a1, a2, b1, b2):
        line_segment_a = (a1, a2)
        line_segment_b = (b1, b2)

        # Nel caso in cui un estremo sia uguale per due segmenti allora ci va bene!
        if (a2 == b1) or (a1 == b2):
            return False

        if intx.do_bounding_boxes_intersect(a1, a2, b1, b2) \
                and intx.line_segment_crosses_line(line_segment_a, line_segment_b) \
                and intx.line_segment_crosses_line(line_segment_b, line_segment_a):
            print(f"Found intersection between: {self.get_node_from_coords(a2)} - {self.get_node_from_coords(a1)} "
                  f"and {self.get_node_from_coords(b2)} - {self.get_node_from_coords(b1)}")

            return True

        return False

    def generate_edges(self, central_node):
        """
        Generates the edges of the given graph starting from central_node and finding the nearest node to it. Then
        recursively applies the function to the new central_node until there are no more connections left in the graph

        """

        distance_ordered_nodes = self.find_nearest_node(central_node)

        if distance_ordered_nodes is None:  # No other nodes available
            return

        if len(self.edges) < 2:  # No need to check for intersections
            self.build_edge(central_node, distance_ordered_nodes[0])
            self.get_status(central_node, distance_ordered_nodes[0])
            self.visualize()

            return self.generate_edges(distance_ordered_nodes[0])

        for node, _ in enumerate(distance_ordered_nodes):
            if distance_ordered_nodes[node] is not None:

                if not self.check_edge(central_node, distance_ordered_nodes[node]):
                    if not any(self.do_lines_intersect(self._points[distance_ordered_nodes[node].get_label()],
                                                       self._points[central_node.get_label()], self._points[u],
                                                       self._points[v]) for u, v in self.edges):

                        # self.find_nearest_node(central_node)    #FIXME: serve??
                        self.build_edge(central_node, distance_ordered_nodes[node])
                        self.get_status(central_node, distance_ordered_nodes[node])

                        #TODO: Fai animazione!
                        self.visualize()  # TODO: sarebbe figo se si potesse vedere che disegna comunque l'edge anche se c'è intersezione (in rosso) e poi lo cancella

                        return self.generate_edges(distance_ordered_nodes[node])

                    else:
                        continue

                else:
                    continue

            else:
                return

    def visualize(self):
        """
        Visualization of the graph

        """
        if self.save:
            plt.savefig("graph.png")

        fig = plt.figure()
        plt.figure().clear()
        plt.close()
        plt.clf()

        nx.draw_networkx_edges(self._graph, nx.get_node_attributes(self._graph, 'pos'))
        nx.draw_networkx_nodes(self._graph, nx.get_node_attributes(self._graph, 'pos'), node_color='blue', node_size=180)
        nx.draw_networkx_labels(self._graph, nx.get_node_attributes(self._graph, 'pos'), font_size=10, font_color="white")
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
