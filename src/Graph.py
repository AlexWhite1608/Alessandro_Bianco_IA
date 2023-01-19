import random
import networkx as nx


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


def create_random_nodes(n_nodes):
    """
    Creates n_nodes Node class instances with random x,y coordinates.
    The label string is generated using a random letter + x, y coordinates of the node

    :param: n_nodes (int)
    :return: list of Node

    """
    alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "Z"]
    nodes = []
    for i in range(n_nodes):
        x = random.randint(1, 100)
        y = random.randint(1, 100)
        label = random.choice(alphabet) + '_' + str(x) + str(y)
        nodes.append(Node(label, x, y))

    return nodes


class Graph:

    def __init__(self, n_nodes):
        self.n_nodes = n_nodes
        self._nodes = create_random_nodes(self.n_nodes)

        self._graph = nx.Graph()
        self._graph.add_nodes_from(self._nodes)

    def add_node(self, node):
        if node not in self._nodes:
            self._nodes.append(node)

    def remove_node(self, node):
        if node in self._nodes:
            self._nodes.remove(node)

    def __str__(self):
        res = "--- Nodes ---"

        res += "\n"
        for node in self._nodes:
            res += str(node.get_label()) + ": "
            res += "x: " + str(node.get_x())
            res += " y: " + str(node.get_y()) + "\n"

        return res
