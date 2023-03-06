import math
import random
import networkx as nx
import matplotlib.pyplot as plt
import Intersections as intx
import Backtracking as BT

# Indicates the pause between each edge generation of the graph
PAUSE = 0.5


def create_random_nodes(n_nodes):

    """
    Creates n_nodes Node class instances with random x,y coordinates.

    :param: (int) Number of nodes
    :return: (list) list of Node class instances

    """

    nodes = []
    for i in range(n_nodes):
        x = random.randint(1, 100)
        y = random.randint(1, 100)
        label = str(i)
        nodes.append(Node(label, x, y))

    return nodes


class Node:

    """

    Class that represents each node of the graph.

    Attributes:
        self._x         x coordinate of the node
        self._y         y coordinate of the node
        self._label     label associated with the node

    """

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

    """

    Class that represents the graph

    Attributes:
        self._n_nodes   (int) Number of graph nodes
        self._nodes     (list) List of Node class instances
        self._edges     (list) List of graph edges
        self._save      (bool) True if saves the graph (.png format), False otherwise
        self._points    (dict) Dict containing the coordinates of each node
        self._graph     (networkx Graph) Stores the networkx Graph information

    """

    def __init__(self, n_nodes, save=False):

        """
        Builds the graph given n_nodes Nodes. It also sets the coordinates from each node to be used for the
        graph generation

        :param n_nodes  (int)
        :param save     (bool) True if saves the graph (.png format), False otherwise

        """

        self._n_nodes = n_nodes
        self._nodes = create_random_nodes(self._n_nodes)
        self._edges = []
        self._save = save
        self._points = self.get_node_coords()
        self._graph = nx.Graph()

        for node in self._nodes:
            pos_x = node.get_x()
            pos_y = node.get_y()
            self._graph.add_node(node.get_label(), pos=(pos_x, pos_y))

        pos = self.get_node_coords()
        nx.set_node_attributes(self._graph, pos, 'coord')

    def get_status(self, current_node, nearest_node):

        """
        Print all the useful data for each edge generation step

        :param current_node: (Node) Node class instance that represents the current node of the generation
        :param nearest_node: (Node) Node class instance that represents the nearest node from current_node

        """

        print("\nCurrent node:", current_node.get_label(), f"{self._points[current_node.get_label()]}")
        print("Nearest node:", nearest_node.get_label(), f"{self._points[nearest_node.get_label()]}")
        print("Edge between:", current_node.get_label(), "-", nearest_node.get_label())

    def get_random_node(self):

        """

        Returns a random node from the list of the graph nodes

        :return: (Node)

        """

        return random.choice(self._nodes)

    def check_edge(self, node1, node2):

        """

        Check if there is an edge between node1 and node2

        :param node1: (Node)
        :param node2: (Node)
        :returns: True if there is an edge between the two nodes, False otherwise

        """

        edge1 = tuple((node1.get_label(), node2.get_label()))
        edge2 = tuple((node2.get_label(), node1.get_label()))

        if edge1 in self._edges or edge2 in self._edges:
            return True
        else:
            return False

    def find_nearest_node(self, input_node):

        """

        Computes the Euclidean distance from input_node to all the other nodes of the graph to find the (ascending)
        ordered nearest nodes

        :param input_node: (Node)
        :return: (list) List of the nearest nodes from input_node

        """

        node_distance = {}
        for node in self._nodes:
            if input_node != node:
                if not self.check_edge(input_node, node):  # if there is already an edge skip
                    node_distance[node.get_label()] = math.dist((input_node.get_x(), input_node.get_y()),
                                                                  (node.get_x(), node.get_y()))

        if len(node_distance) == 0:  # if there are no edges left return None --> ends generate_edges recursion
            return None

        sorted_node_distances = sorted(node_distance, key=node_distance.get)

        # a list containing the nearest nodes to input_node sorted by distance
        distance_ordered_nodes = []

        for x in sorted_node_distances:
            for node in self._nodes:
                if x == node.get_label():
                    distance_ordered_nodes.append(node)

        return distance_ordered_nodes

    def get_node_coords(self):

        """

        Gets the coordinates of each node stored in a dictionary

        :return: (dict) dict containing key: node, value: tuple of x,y coordinates

        """

        node_coords = {}
        for node in self._nodes:
            node_coords[node.get_label()] = tuple((node.get_x(), node.get_y()))

        return node_coords

    def get_node_from_coords(self, coords):

        """

        Gets the node corresponding to the given coordinates

        :param coords: (tuple) Tuple of x, y coordinates of the node
        :return: (Node)

        """

        for node, coordinates in self._points.items():
            if coords == coordinates:
                return node

    def build_edge(self, node1, node2):

        """

        Builds an edge between node1 and node2 if they are not the same node

        :param node1: (Node)
        :param node2: (Node)

        """

        # Add edge to networkx Graph and to self._edges attribute
        if node1 is not node2:
            self._graph.add_edge(node1.get_label(), node2.get_label())
            edge = tuple((node1.get_label(), node2.get_label()))

            if edge not in self._edges:
                self._edges.append((node1.get_label(), node2.get_label()))

    def do_lines_intersect(self, a1, a2, b1, b2):

        """

        Check if the lines generated by the nodes intersect

        :param a1: (tuple) Starting node of the first line coordinates
        :param a2: (tuple) Ending node of the first line coordinates
        :param b1: (tuple) Starting node of the second line coordinates
        :param b2: (tuple) Ending node of the second line coordinates
        :return: True if the two lines intersect, False otherwise

        """

        line_segment_a = (a1, a2)
        line_segment_b = (b1, b2)

        # No intersection if the ending node of the first line is equal to the starting node of the second line
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

        Generates the edges of the graph starting from central_node and finding the nearest node to it
        (first element of the list of the nearest nodes). Then recursively applies the function to the new central_node
        until there are no more connections left in the graph

        """

        distance_ordered_nodes = self.find_nearest_node(central_node)

        if distance_ordered_nodes is None:  # No other nodes available
            return

        if len(self._edges) < 2:  # No need to check for intersections
            self.build_edge(central_node, distance_ordered_nodes[0])
            self.get_status(central_node, distance_ordered_nodes[0])
            self.visualize()

            return self.generate_edges(distance_ordered_nodes[0])

        for node, _ in enumerate(distance_ordered_nodes):
            if distance_ordered_nodes[node] is not None:

                if not self.check_edge(central_node, distance_ordered_nodes[node]):
                    if not any(self.do_lines_intersect(self._points[distance_ordered_nodes[node].get_label()],
                                                       self._points[central_node.get_label()], self._points[u],
                                                       self._points[v]) for u, v in self._edges):

                        self.build_edge(central_node, distance_ordered_nodes[node])
                        self.get_status(central_node, distance_ordered_nodes[node])

                        # TODO: Fai animazione!
                        # TODO: sarebbe figo se si potesse vedere che disegna comunque l'edge anche se c'è intersezione (in rosso) e poi lo cancella
                        self.visualize()

                        return self.generate_edges(distance_ordered_nodes[node])

                    else:
                        continue    # Found intersection

                else:
                    continue    # There is already an edge between central_node and nearest node

            else:
                return

    def backtracking(self, bt_type):

        """

        Backtracking algorithm to find the graph-colouring solution in two different ways (FC/MAC)

        :param bt_type: (String) "ForwardChecking" or "Mac"

        """

        # Initialize the graph dict: {node: [neighbors]}
        graph = {}
        for node, neighbor in self._graph.adjacency():
            graph[node] = list(neighbor.keys())

        # The initial assignment consists of all the available colors assigned to all nodes
        initial_assignment = {}
        for node in graph:
            initial_assignment[node] = list(BT.COLORS)

        if bt_type == "ForwardChecking":
            return BT.backtrack_fc(self._graph, graph, initial_assignment, self._nodes)
        elif bt_type == "Mac":
            return BT.backtrack_mac(self._graph, graph, initial_assignment, self._nodes)

    def visualize(self):

        """

        Visualization of the graph

        """

        if self._save:
            plt.savefig("graph.png")

        fig = plt.figure()
        plt.figure().clear()
        plt.close()
        plt.clf()

        nx.draw_networkx_edges(self._graph, nx.get_node_attributes(self._graph, 'pos'))
        nx.draw_networkx_nodes(self._graph, nx.get_node_attributes(self._graph, 'pos'), node_color='black', node_size=180)
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
