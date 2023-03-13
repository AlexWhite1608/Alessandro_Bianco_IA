import time

import Graph as Graph
from testBT import test1

# CONST VALUES #
N_NODES = 8
ANIMATION = True
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
    # # print("FC: ", graph.backtracking("ForwardChecking"))
    # print("Mac: ", graph.backtracking("Mac"))

    # test1.time_performance_test()
    test1.test_timeit()


if __name__ == "__main__":
    main()
