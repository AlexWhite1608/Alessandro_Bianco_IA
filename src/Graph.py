import math
import random
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation

# Const values
PAUSE = 1.5

def create_random_nodes(n_nodes):
    """
    Creates n_nodes Node class instances with random x,y coordinates.
    The label string is generated using a random letter + x, y coordinates of the node

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
                if not self.check_edge(input_node, _node):
                    _node_distance[_node.get_label()] = math.dist((input_node.get_x(), input_node.get_y()),
                                                                  (_node.get_x(), _node.get_y()))

        if len(_node_distance) != 0:    # if there are no edges left return None --> ends generate_edges recursion
            min_label = min(_node_distance, key=_node_distance.get)
        else:
            return None, None

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

    def generate_edges(self, central_node):  # FIXME: non devi usare visited nodes perchè ti fermi prima di aver finito tutte le connessioni!
        """
        Generates the edges of the given graph starting from central_node and finding the nearest node to it. Then
        recursively applies the function to the new central_node until there are no more connections left in the graph

        :param: central_node (Node)
        :param: visited_nodes (list of Nodes)
        :return: a list of edges

        """

        # TODO: CONTROLLA INCROCI!

        nearest_node, distances = self.find_nearest_node(central_node)

        if nearest_node is not None and not self.check_edge(central_node, nearest_node):

            self.build_edge(central_node, nearest_node)
            get_status(central_node, nearest_node, distances)
            self.visualize()
            return self.generate_edges(nearest_node)

        else:
            return

    def visualize(self):
        """
        Visualization of the given graph

        """
        if self.save:
            plt.savefig("graph.png")

        # nx.draw(self._graph, nx.get_node_attributes(self._graph, 'pos'), with_labels=True, **options)

        # nx.draw_networkx_edges(self._graph, nx.get_node_attributes(self._graph, 'pos'))
        # nx.draw_networkx_nodes(self._graph, nx.get_node_attributes(self._graph, 'pos'), node_color='green')
        # nx.draw_networkx_labels(self._graph, nx.get_node_attributes(self._graph, 'pos'), font_size=13)

        plt.clf()
        nx.draw_networkx_edges(self._graph, nx.get_node_attributes(self._graph, 'pos'))
        nx.draw_networkx_nodes(self._graph, nx.get_node_attributes(self._graph, 'pos'), node_color='green')
        nx.draw_networkx_labels(self._graph, nx.get_node_attributes(self._graph, 'pos'), font_size=13)
        plt.show()
        plt.pause(PAUSE)

        # fig, ax = plt.subplots()
        # ani = matplotlib.animation.FuncAnimation(fig, self.update_graph(), frames=self.n_nodes, interval=1000, repeat=True)

    def __str__(self):
        res = "--- Nodes ---"

        res += "\n"
        for node in self._nodes:
            res += str(node.get_label()) + ": "
            res += "x: " + str(node.get_x())
            res += " y: " + str(node.get_y()) + "\n"

        return res
