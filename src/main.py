import time

from matplotlib import pyplot as plt
from Backtracking import COLORS
import Graph as Graph
from testBT import test1

# CONST VALUES #
N_NODES = 18
ANIMATION = True
SYMMETRICAL = False


def main():
    # graph = Graph.Graph(N_NODES, ANIMATION, SYMMETRICAL)
    # print(graph)
    #
    # random_node1 = graph.get_random_node()
    # print("Starting node: ", random_node1.get_label())
    #
    # graph.generate_edges(random_node1)
    #
    # # graph.backtracking("ForwardChecking")
    # graph.backtracking("Mac")

    # TEST
    test1.comparison_k3_k4()


if __name__ == "__main__":
    main()
