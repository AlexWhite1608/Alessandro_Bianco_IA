import time
from Backtracking import COLORS
import Graph as Graph
from testBT import test1

# CONST VALUES #
N_NODES = 30
ANIMATION = False
SYMMETRICAL = False


def main():
    # graph = Graph.Graph(N_NODES, ANIMATION, SYMMETRICAL)
    # print(graph)
    #
    # random_node1 = graph.get_random_node()
    # print("RANDOM: ", random_node1.get_label())
    #
    # graph.generate_edges(random_node1)
    #
    # print("FC: ", graph.backtracking("ForwardChecking"))
    # # print("Mac: ", graph.backtracking("Mac"))

    # test1.time_performance_test()
    test1.comparison_k3_k4()


if __name__ == "__main__":
    main()
